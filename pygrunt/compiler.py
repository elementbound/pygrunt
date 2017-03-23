class Compiler:
    def __init__(self):
        self.executable_path = None
        self.unique_flags = {}

    def _build_defs(self, definitions):
        pass

    def _build_flags(self, flags):
        return ['-'+f for f in flags]

    def compile_object(self, in_file, out_file, additional_args=[]):
        import subprocess

        print('Compiling', in_file, '->', out_file, end='... ')
        self._args.extend(self.unique_flags.values())
        self._args.extend(additional_args)
        result = subprocess.run(self._args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        print('success' if result.returncode == 0 else 'fail')

        # TODO: do something useful with output
        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)

        return result.returncode == 0

    def link_executable(self, in_files, out_file):
        import subprocess

        print('Linking', out_file, '... ')
        result = subprocess.run(self._args)
        return result.returncode == 0

    def compile_project(self, project):
        import os.path

        project.sanitize()

        # Go through each source file and then link them
        object_files = []
        additional_args = self._build_defs(project.definitions)
        additional_args.extend(self._build_flags(project.flags))

        for file in project.sources:
            in_file = os.path.realpath(file)
            in_file = os.path.relpath(in_file, project.working_dir)

            # TODO: Something that's not this dumb
            out_file = os.path.join('build/', in_file)
            out_file = os.path.splitext(out_file)[0] + '.o'
            out_dir = os.path.dirname(out_file)

            # Create path for output file if it does not exist
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            # Fail if one of the files doesn't compile
            if not self.compile_object(file, out_file, additional_args):
                return False

            object_files.append(out_file)

        # Produce executable
        self.link_executable(object_files, project.executable)

class CompilerNotFoundException(Exception):
    pass

class GCCCompiler(Compiler):
    def __init__(self, executable_path=None):
        import os

        super().__init__()

        self.executable_path = executable_path
        if self.executable_path is None:
            # Look for GCC in path
            path = os.environ['PATH']
            path = path.split(';')

            print('Looking for GCC on PATH... ')
            for dir in path:
                if os.path.isfile(dir+'/gcc.exe'):
                    self.executable_path = dir+'/gcc.exe'
                    print('Found GCC at', dir)
                    break

        # Check if the executable exists
        if not os.path.isfile(self.executable_path):
            raise CompilerNotFoundException()

    def _build_defs(self, definitions):
        return ['-D'+x + ('='+y if y is not None else '') for x,y in definitions.items()]

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
        
    def compile_object(self, in_file, out_file, additional_args=[]):
        self._args = [self.executable_path, '-c', in_file, '-o', out_file]
        return super().compile_object(in_file, out_file, additional_args)

    def link_executable(self, in_files, out_file):
        self._args = [self.executable_path]
        self._args.extend(in_files)
        self._args.extend(['-o', out_file])
        self._args.extend(self.unique_flags.values())

        return super().link_executable(in_files, out_file)
