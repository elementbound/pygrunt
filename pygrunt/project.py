import collections
from .fileset import FileSet, DirectorySet

class Project:
    def __init__(self, name):
        self.name = name

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

    # Include directories
    def add_include_dir(self, directory):
        import os.path
        if not os.path.isabs(directory):
            directory = os.path.join(self.working_dir, directory)
            directory = os.path.realpath(directory)

        if dir not in self.include_dirs:
            self.include_dirs.append(directory)

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

    # For now accept a single parameter and glob
    def add_sources(self, sources, recursive=False):
        from glob import glob
        import os

        files = glob(sources, recursive=recursive)
        if not files:
            files = glob(self.working_dir+'/'+sources, recursive = recursive)
        if not files:
            print('Pattern did not match:', sources)

        self.sources.extend(files)

    # Set some sane defaults
    def sanitize(self):
        import os.path

        if not self.working_dir:
            self.working_dir = os.path.curdir

        if not self.output_dir:
            self.output_dir = os.path.join(self.working_dir, 'build', '')

        if not self.executable:
            self.executable = os.path.join(self.output_dir, self.name)

        allowed_types = ['executable', 'library']
        if self.type not in allowed_types:
            # TODO: exceptions?
            print('Invalid output type:', self.type)
            print('Allowed types:', allowed_types)
            self.type = allowed_types[0]
            print('Reverting to', self.type)

        self.working_dir = os.path.realpath(self.working_dir)
        self.output_dir = os.path.realpath(self.output_dir)
