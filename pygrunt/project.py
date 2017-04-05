import collections
from pathlib import Path
from .style import Style
from .fileset import FileSet, DirectorySet

class BarebonesProject:
    def __init__(self, name=None):
        self.name = name if name is not None else self.__class__.__name__

        self.sources = FileSet()
        self.definitions = {}
        self.flags = {}
        self.include_dirs = DirectorySet()
        self.linker_flags = []
        self.libraries = collections.OrderedDict()
        self.working_dir = None
        self.output_dir = None

        self.executable = None
        self.type = 'executable'

        self.stages = []

    # Defines
    def define(self, name, value=None):
        self.definitions[name] = value

    def undefine(self, name):
        del self.definitions[name]

    # Compiler flags
    def flag(self, flag):
        self.flags[flag] = True

    def unflag(self, flag):
        del self.flags[flag]

    # Libraries to link
    def link(self, *args):
        for library in args:
            self.libraries[library] = True

    def unlink(self, *args):
        for library in args:
            del self.libraryies[library]

    # Set some sane defaults
    def sanitize(self):
        import os.path
        import platform

        if not self.working_dir:
            self.working_dir = os.path.curdir

        if not self.output_dir:
            self.output_dir = os.path.join(self.working_dir, 'build', '')

        allowed_types = ['executable', 'library', 'shared']
        if self.type not in allowed_types:
            # TODO: exceptions?
            print('Invalid output type:', self.type)
            print('Allowed types:', allowed_types)
            self.type = allowed_types[0]
            print('Reverting to', self.type)

        if not self.executable:
            if self.type == 'executable':
                if platform.system() == 'Windows':
                    self.executable = os.path.join(self.output_dir, self.name+'.exe')
                else:
                    self.executable = os.path.join(self.output_dir, self.name)
            elif self.type == 'library':
                self.executable = os.path.join(self.output_dir, 'lib'+self.name.lower()+'.a')
            elif self.type == 'shared':
                if platform.system() == 'Windows':
                    self.executable = os.path.join(self.output_dir, 'lib'+self.name.lower()+'.dll')
                else:
                    self.executable = os.path.join(self.output_dir, 'lib'+self.name.lower()+'.so')

        self.working_dir = os.path.realpath(self.working_dir)
        self.output_dir = os.path.realpath(self.output_dir)

        self.sources.working_directory = Path(self.working_dir)

    def run(self):
        Style.title('Building', self.name)

        for idx, stage in enumerate(self.stages):
            Style.title('[{0}/{1}]'.format(idx+1, len(self.stages)), 'Running stage', stage.__name__)
            stage()


class Project(BarebonesProject):
    def __init__(self, name=None):
        super().__init__(name)

        self.stages = [
            self.init,
            self.gather,
            self.validate,
            self.preprocess,
            self.compile,
            self.install
        ]

        # Filter out non-overloaded stages, since those do nothing
        for stage in self.stages:
            name = stage.__name__
            if  getattr(self.__class__, name) == getattr(Project, name):
                self.stages.remove(stage)

    def run(self):
        Style.title('Building', self.name)

        for idx, stage in enumerate(self.stages):
            Style.title('[{0}/{1}]'.format(idx+1, len(self.stages)), 'Running stage', stage.__name__)

            # Additional behaviour here...
            # TODO: Solve this in a much less hacky way
            if stage.__name__ == 'compile':
                cachefile = str(Path(self.output_dir, 'recompile.cache'))

                # Try loading recompile cache
                self.compiler.recompile.load_cache(cachefile)

                stage()

                # Save recompile cache
                self.compiler.recompile.save_cache(cachefile)
            else:
                stage()

    # Stages:
    def init(self):
        pass

    def gather(self):
        pass

    def validate(self):
        pass

    def preprocess(self):
        pass

    def compile(self):
        pass

    def install(self):
        pass
