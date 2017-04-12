import pygrunt.platform as platform
from pygrunt import Style, FileSet

class CythonNotFoundException(Exception):
    pass

class Cython:
    def __init__(self):
        import os

        self.executable = platform.current.find_executable('cython')
        if self.executable is None:
            raise CythonNotFoundException()

        self.working_directory = os.curdir
        self.debug = False
        self.cpp = False
        self.python = None

    @classmethod
    def add_to(klass, project, compile_generated=True):
        cy = Cython()
        cy.working_directory = project.working_dir

        project.cython = cy
        project.cython_sources = FileSet()

        def cython_preprocess(project):
            out_sources = []

            # TODO: Move this to a file_loop function in Project
            for idx, file in enumerate(self.sources):
                in_file = file.resolve()
                in_file = in_file.relative_to(self.working_dir)

                out_file = Path(self.output_dir, 'cython', in_file)
                out_file = Path(Cython.as_source(out_file))
                out_dir = out_file.parent

                # Create path for output file if it does not exist
                out_dir.mkdir(parents=True, exist_ok=True)

                # Print what's happening
                print_in = str(in_file)
                print_out = str(out_file.relative_to(self.output_dir))
                print('[{0:3.0f}%]'.format((idx+1)/len(self.sources)*100), end=' ')
                Style.object('Processing', in_file, '->', print_out)

                # Fail if one of the files doesn't compile
                if not self.cython.process(str(file), out_file):
                    raise StageFailException(__name__)

                out_sources.append(out_file)

            if compile_generated:
                project.sources += out_sources

        def cython_hook(fn, project):
            def _hook(project):
                cython_preprocess(project)
                fn()

            return _hook

        try:
            project.hook_stage('preprocess', cython_hook)
        except:
            # TODO: This is a bullshit limitation
            Style.error('Trying to add Cython to a project with no preprocess stage')
            Style.error('Please add a dummy preprocess stage')

    def process(self, in_file, out_file):
        import subprocess

        arg_settings = ['-w', self.working_directory]
        if self.debug:
            arg_settings.append('--gdb')

        if self.cpp:
            arg_settings.append('--cplus')

        if self.python == 2:
            arg_settings.extend('-2')
        elif self.python == 3:
            arg_settings.extend('-3')
        elif self.python == None:
            pass
        else:
            Style.warning('Can\'t compile for Python version', self.python)
            Style.warning('Skipping flag')

        args = ['cython'] + arg_settings + [in_file, '-o', out_file]

        result = subprocess.run(args)
        if result.returncode != 0:
            Style.error('Cython failed')
            return False

        return True

    @staticmethod
    def as_module(filename):
        if platform.Windows():
            return str(Path(filename).with_suffix('.pyd'))
        else:
            return str(Path(filename).with_suffix('.so'))

    @staticmethod
    def as_source(filename):
        return str(Path(filename))+'.c'
