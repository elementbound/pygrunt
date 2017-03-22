class Compiler:
    def __init__(self):
        self.executable_path = ''

    def compile_file(self, in_file, out_file):
        pass

    def compile_project(self, project):
        pass

class CompilerNotFoundException(Exception):
    pass

class GCCCompiler(Compiler):
    def __init__(self, executable_path=None):
        import os

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

    def compile_file(self, in_file, out_file):
        import subprocess

        print('Compiling', in_file, '->', out_file, end='... ')
        args = [self.executable_path, in_file, '-o', out_file]
        result = subprocess.run(args)

        if result.returncode == 0:
            print('success')
            return True
        else:
            print('fail')
            return False
