from pathlib import Path
from .style import Style
from .fileset import FileSet, DirectorySet
import pygrunt.platform as platform
import pygrunt # args

class StageFailException(Exception):
    def __init__(self, stage):
        self.stage = stage
        super().__init__("Stage \"{0}\" failed".format(stage))


class StageSkipException(Exception):
    def __init__(stage):
        self.stage = stage
        super().__init__("Stage \"{0}\" requested skip".format(stage))


class BarebonesProject:
    def __init__(self, name=None):
        self.name = name if name is not None else self.__class__.__name__

        self.sources = FileSet()

        self.working_dir = None
        self.output_dir = None

        self.executable = None
        self.type = 'executable'

        self.stages = []

        # TODO: Possibly private?
        self.stage_hooks = {}

    # Set some sane defaults
    def sanitize(self):
        import os.path

        if not self.working_dir:
            self.working_dir = os.path.curdir

        if not self.output_dir:
            self.output_dir = os.path.join(self.working_dir, 'build', '')

        allowed_types = ['executable', 'library', 'shared']
        if self.type not in allowed_types:
            # TODO: exceptions?
            Style.error('Invalid output type:', self.type)
            Style.error('Allowed types:', allowed_types)
            self.type = allowed_types[0]
            Style.error('Reverting to', self.type)

        if not self.executable:
            self.executable = os.path.join(self.output_dir, self.name)

        if self.type == 'executable':
            self.executable = platform.current.as_executable(self.executable)
        elif self.type == 'library':
            self.executable = platform.current.as_static_library(self.executable)
        elif self.type == 'shared':
            self.executable = platform.current.as_shared_library(self.executable)

        self.working_dir = os.path.realpath(self.working_dir)
        self.output_dir = os.path.realpath(self.output_dir)

        self.sources.working_directory = Path(self.working_dir)

        self._init_hooks()

    # Stage hooks

    # Create an empty list for each stage
    def _init_hooks(self):
        for stage in self.stages:
            self.stage_hooks[stage.__name__] = []

    def _hook_key(self, stage):
        if type(stage) is str:
            return stage
        else:
            return stage.__name__

    def _hooks_for_stage(self, stage):
        stage = self._hook_key(stage)
        try:
            return self.stage_hooks[stage]
        except KeyError:
            return []

    def hook_stage(self, stage, hook):
        self.stage_hooks[self._hook_key(stage)].append(hook)

    def unhook_stage(self, stage, hook):
        self.stage_hooks[self._hook_key(stage)].remove(hook)

    # Run project
    def run(self):
        Style.title('Building', self.name)

        for idx, stage in enumerate(self.stages):
            Style.title('[{0}/{1}]'.format(idx+1, len(self.stages)), 'Running stage', stage.__name__)

            try:
                # Apply all decorators
                hooks = self._hooks_for_stage(stage)
                hooked_stage = stage

                for hook in hooks:
                    hooked_stage = hook(hooked_stage, self)

                # Call the stage with all its hooks
                hooked_stage()
            except StageFailException:
                Style.error('Stage', stage.__name__, 'failed!')
                return False
            except StageSkipException:
                pass

        return True


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

        # Check if the class we are initializing is overridden
        # If it's not, a simple build function is used to build the project, thus no need to
        # filter stages and warn about them

        if self.__class__ == __class__:
            return

        # Stages that can be absent
        optional_stages = ['validate', 'preprocess', 'install']

        # Stages that are empty and should be overridden ( if not optional )
        empty_stages = ['init', 'gather', 'validate', 'preprocess', 'install']

        # Check stages
        # Filter out optional non-overloaded stages, these do nothing
        # Warn about non-overloaded stages that should be overloaded
        # Note: iterating in reverse because we delete from the list as we go
        for stage in reversed(self.stages):
            name = stage.__name__

            if  getattr(self.__class__, name) == getattr(Project, name):
                # Optional stages are okay if left out
                if stage.__name__ in optional_stages:
                    self.stages.remove(stage)
                    continue

                # Non-optional empty stages should be overridden though
                if stage.__name__ in empty_stages:
                    self.stages.remove(stage)
                    Style.warning('Stage', stage.__name__, 'is empty. Did you forget to override it?')

        # Add stage hooks

        self._init_hooks()

        def cache_hook(fn, project):
            def _hook():
                cachefile = str(Path(project.output_dir, 'recompile.cache'))

                # Try loading recompile cache
                project.compiler.recompile.load_cache(cachefile)

                fn()

                # Save cache
                project.compiler.recompile.save_cache(cachefile)

            return _hook

        self.hook_stage('compile', cache_hook)

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
        import os.path

        if self.compiler is None:
            Style.error('No compiler to use!')
            raise StageFailException(__name__)

        self.sanitize()
        cc = self.compiler

        Style.info('Source directory is', self.working_dir)
        Style.info('Build directory is', self.output_dir)

        # Try loading cache for self.recompile
        cc.recompile.load_cache(os.path.join(self.output_dir, 'recompile.cache'))
        if pygrunt.args.clear_cache:
            cc.recompile.clear_cache()

        # Go through each source file and then link them
        object_files = []

        for idx, file in enumerate(self.sources):
            # TODO: pathlib.Path instead of os.path
            in_file = str(file)
            in_file = os.path.relpath(in_file, self.working_dir)

            out_file = os.path.join(self.output_dir, in_file)
            out_file = platform.current.as_object(out_file)
            out_dir = os.path.dirname(out_file)

            # Create path for output file if it does not exist
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            # Print what's happening
            print_in = in_file
            print_out = os.path.relpath(out_file, self.output_dir)
            print('[{0:3.0f}%]'.format((idx+1)/len(self.sources)*100), end=' ')
            Style.object('Compiling', in_file, '->', print_out)

            # Fail if one of the files doesn't compile
            if not cc.compile_object(str(file), out_file):
                raise StageFailException(__name__)

            object_files.append(out_file)

        # Save compile cache
        cc.recompile.save_cache(os.path.join(self.output_dir, 'recompile.cache'))

        # Produce executable
        if self.type == 'executable':
            cc.link_executable(object_files, self.executable)
        elif self.type == 'library' or self.type == 'shared':
            cc.link_library(object_files, self.executable)
        else:
            Style.error('Can\'t produce', self.type)

    def install(self):
        pass
