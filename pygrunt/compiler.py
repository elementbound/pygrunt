from .style import Style
from .fileset import FileSet, DirectorySet
import pygrunt.recompile as recompile
import pygrunt.platform as platform
import collections

class Compiler:
    def __init__(self):
        self.executable_path = None

        self.definitions = {}
        self.flags = {}
        self.include_dirs = DirectorySet()
        self.linker_flags = []
        self.library_dirs = DirectorySet()
        self.libraries = collections.OrderedDict()

        self.unique_flags = {}

        self.recompile = recompile.PreprocessHash(self)

    def _build_defs(self, definitions):
        raise NotImplementedError()

    def _build_flags(self, flags):
        return ['-'+f for f in flags]

    def _build_unique_flags(self):
        return [value for value in self.unique_flags.values() if value is not None]

    def _build_library_links(self, libs):
        raise NotImplementedError()

    def _build_library_dirs(self, dirs):
        raise NotImplementedError()

    def _build_user_linker_flags(self, flags):
        return self._build_flags(flags)

    def _build_includes(self, includes):
        raise NotImplementedError()

    def _build_compiler_flags(self):
        flags = self._build_defs(self.definitions)
        flags.extend(self._build_flags(self.flags))
        flags.extend(self._build_unique_flags())
        flags.extend(self._build_includes(self.include_dirs.strings()))

        return flags

    def _build_linker_flags(self):
        flags = self._build_flags(self.flags) # These flags could also concern the linker
        flags.extend(self._build_unique_flags()) # These too
        flags.extend(self._build_library_dirs(self.library_dirs))
        flags.extend(self._build_user_linker_flags(self.linker_flags))
        flags.extend(self._build_library_links(self.libraries))

        return flags

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
            del self.libraries[library]

    # Operations
    def preprocess_source(self, in_file, additional_args=[]):
        import subprocess

        self._args.extend(self._build_compiler_flags())
        self._args.extend(additional_args)

        result = subprocess.run(self._args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if result.returncode == 0:
            return result.stdout
        else:
            if result.stderr:
                Style.error('Preprocess failed: ')
                print(result.stderr)

            return ''

    def compile_object(self, in_file, out_file):
        import subprocess
        import os.path

        # Skip compile if RecompileStrategy says so
        # Since preprocess_source ( possibly used by recompile ) also modifies self._args,
        # we gotta back it up
        # TODO: Maybe use something more elegant than self._args?
        old_args = self._args
        if os.path.isfile(out_file):
            if not self.recompile.should_recompile(in_file):
                Style.info('Nothing to do with', in_file)
                return True
        self._args = old_args

        self._args.extend(self._build_compiler_flags())
        result = subprocess.run(self._args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # TODO: do something useful with output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result.returncode == 0

    def link_executable(self, in_files, out_file):
        import subprocess

        Style.link('Linking executable', out_file, '... ')
        self._args.extend(self._build_linker_flags())
        result = subprocess.run(self._args)
        return result.returncode == 0

    def link_library(self, in_files, out_file):
        import subprocess

        Style.link('Linking library', out_file)
        self._args.extend(self._build_linker_flags())
        result = subprocess.run(self._args)
        return result.returncode == 0

    def compile_project(self, project):
        Style.warning('Compiler.compile_project() is deprecated! Use Project.compile() instead.')
        project.compiler = self
        return project.compile()

class CompilerNotFoundException(Exception):
    pass

class GCCCompiler(Compiler):
    def __init__(self, executable_path=None, cpp=False):
        import os

        super().__init__()

        self.executable_path = executable_path
        if self.executable_path is None:
            # Look for GCC in path
            path = platform.current.path()

            compiler_name = 'g++' if cpp else 'gcc'
            compiler_name = platform.current.as_executable(compiler_name)

            self.executable_path = platform.current.find_executable(compiler_name)

        # Check if the executable exists
        if not os.path.isfile(self.executable_path):
            raise CompilerNotFoundException()

    def _build_defs(self, definitions):
        return ['-D'+x + ('='+y if y is not None else '') for x,y in definitions.items()]

    def _build_library_links(self, libs):
        return ['-l'+x for x in libs]

    def _build_library_dirs(self, dirs):
        return ['-L'+str(x) for x in dirs]

    def _build_includes(self, includes):
        return ['-I'+i for i in includes]

    def optimize(self, mode):
        mode_to_flag = {
            'none': '-O0',
            'optimize': '-O1',
            'more': '-O2',
            'most': '-O3',
            'size': '-Os',
            'debug': '-Og',
            'fast': '-Ofast'
        }

        if mode not in mode_to_flag:
            # TODO: exception instead of print
            print('Unknown optim mode:', mode)
            print('Allowed modes:', ', '.join(mode_to_flag.keys()))
            return False

        self.unique_flags['optimize'] = mode_to_flag[mode]
        return True

    def standard(self, std):
        if std == None:
            del self.unique_flags['std']
        else:
            self.unique_flags['std'] = '-std='+std

    def preprocess_source(self, in_file, additional_args=[]):
        self._args = [self.executable_path, '-E', in_file]
        return super().preprocess_source(in_file, additional_args)

    def compile_object(self, in_file, out_file):
        self._args = [self.executable_path, '-c', in_file, '-o', out_file]
        return super().compile_object(in_file, out_file)

    def link_executable(self, in_files, out_file):
        self._args = [self.executable_path]
        self._args.extend(in_files)
        self._args.extend(['-o', out_file])
        self._args.extend(self.unique_flags.values())

        return super().link_executable(in_files, out_file)

    def link_library(self, in_files, out_file):
        self._args = [self.executable_path, '-shared']
        self._args.extend(in_files)
        self._args.extend(['-o', out_file])
        self._args.extend(self.unique_flags.values())

        return super().link_library(in_files, out_file)

# Return a compiler from the list, don't care which
def any_list(list):
    for compiler in list:
        try:
            return compiler()
        except CompilerNotFoundException:
            pass

    raise CompilerNotFoundException()

# Return a compiler, don't care which
def any():
    return any_list([GCCCompiler])

# Return a C++ compiler, don't care which
def any_cpp():
    # TODO: Figure out how to support more than one, preferably with a list
    try:
        return GCCCompiler(cpp=True)
    except CompilerNotFoundException:
        pass

    raise CompilerNotFoundException()
