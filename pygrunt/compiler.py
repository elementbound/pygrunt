from .style import Style

class Compiler:
    def __init__(self):
        self.executable_path = None
        self.unique_flags = {}

    def _build_defs(self, definitions):
        pass

    def _build_flags(self, flags):
        return ['-'+f for f in flags]

    def _build_unique_flags(self):
        return [value for value in self.unique_flags.values() if value is not None]

    def _build_library_links(self, libs):
        pass

    def _build_includes(self, includes):
        pass

    def compile_object(self, in_file, out_file, print_name=None, additional_args=[]):
        import subprocess

        if print_name is None:
            print_name = in_file

        #print(Style.object('Compiling', print_name, '->', out_file, '... '))
        self._args.extend(self._build_unique_flags())
        self._args.extend(additional_args)
        result = subprocess.run(self._args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # TODO: do something useful with output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result.returncode == 0

    def link_executable(self, in_files, out_file):
        import subprocess

        print(Style.link('Linking executable', out_file, '... '))
        result = subprocess.run(self._args)
        return result.returncode == 0

    def link_library(self, in_files, out_file):
        import subprocess

        print(Style.link('Linking library', out_file))
        result = subprocess.run(self._args)
        return result.returncode == 0

    def compile_project(self, project):
        import os.path

        project.sanitize()

        print('Source directory is', project.working_dir)
        print('Build directory is', project.output_dir)

        # Go through each source file and then link them
        object_files = []
        additional_args = self._build_defs(project.definitions)
        additional_args.extend(self._build_flags(project.flags))
        additional_args.extend(self._build_includes(project.include_dirs))

        for idx, file in enumerate(project.sources):
            in_file = str(file) # os.path.realpath(file)
            in_file = os.path.relpath(in_file, project.working_dir)

            # TODO: Something that's not this dumb
            out_file = os.path.join(project.output_dir, in_file)
            out_file = os.path.splitext(out_file)[0] + '.o'
            out_dir = os.path.dirname(out_file)

            # Create path for output file if it does not exist
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            # Print what's happening
            print_in = in_file
            print_out = os.path.relpath(out_file, project.output_dir)
            print('[{0:3.0f}%]'.format((idx+1)/len(project.sources)*100), end=' ')
            print(Style.object('Compiling', in_file, '->', print_out))

            # Fail if one of the files doesn't compile
            if not self.compile_object(str(file), out_file, additional_args=additional_args):
                return False

            object_files.append(out_file)

        object_files.extend(self._build_library_links(project.libraries))

        # Produce executable
        if project.type == 'executable':
            self.link_executable(object_files, project.executable)
        elif project.type == 'library':
            self.link_library(object_files, project.executable)
        else:
            print('Can\'t produce', project.type)

class CompilerNotFoundException(Exception):
    pass

class GCCCompiler(Compiler):
    def __init__(self, executable_path=None, cpp=False):
        import os
        import platform

        super().__init__()

        self.executable_path = executable_path
        if self.executable_path is None:
            # Look for GCC in path
            path = os.environ['PATH']
            path = path.split(os.pathsep)

            compiler_name = 'g++' if cpp else 'gcc'
            if platform.system() == 'Windows':
                compiler_name += '.exe'

            print('Looking for GCC on PATH... ')
            for dir in path:
                candidate = os.path.join(dir, compiler_name)
                if os.path.isfile(candidate):
                    self.executable_path = candidate
                    print('Found GCC at', self.executable_path)
                    break

        # Check if the executable exists
        if not os.path.isfile(self.executable_path):
            raise CompilerNotFoundException()

    def _build_defs(self, definitions):
        return ['-D'+x + ('='+y if y is not None else '') for x,y in definitions.items()]

    def _build_library_links(self, libs):
        return ['-l'+x for x in libs]

    def _build_includes(self, includes):
        return ['-I'+i for i in includes]

    def optimize(self, mode):
        mode_to_flag = {
            'none': '-O0',
            'optimize': '-O1',
            'more': '-O2',
            'evenmore': '-O3',
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

    def compile_object(self, in_file, out_file, print_name=None, additional_args=[]):
        self._args = [self.executable_path, '-c', in_file, '-o', out_file]
        return super().compile_object(in_file, out_file, print_name, additional_args)

    def link_executable(self, in_files, out_file):
        self._args = [self.executable_path]
        self._args.extend(in_files)
        self._args.extend(['-o', out_file])
        self._args.extend(self.unique_flags.values())

        return super().link_executable(in_files, out_file)

    def link_library(self, in_files, out_file):
        self._args = [self.executable_path, '-shared']
        self._args.extend(in_files)
        self._args.extend(['-o', out_file+'.a'])
        self._args.extend(self.unique_flags.values())

        return super().link_library(in_files, out_file+'.a')

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
