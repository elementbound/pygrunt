class Compiler:
    def __init__(self):
        self.executable_path = ''

    def compile_file(self, in_file, out_file):
        pass

    def compile_project(self, project):
        pass

class GCCCompiler(Compiler):
    def __init__(self, executable_path):
        self.executable_path = executable_path

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
