import pygrunt.platform as platform
from pygrunt import Style, FileSet, StageFailException

from pathlib import Path

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
        project.cython_sources = FileSet(project.working_dir)

        # Try adding Python include- and lib dir
        include_dir = Cython.find_include_dir()
        library = Cython.python_library_file()
        library_dir = Cython.find_lib_dir(library)
        dev_package = [include_dir, library, library_dir]

        if None in dev_package:
            Style.warning('Couldn\'t find Python dev')
            Style.warning('Add these manually so the project compiles')
            Style.info(dev_package)
        else:
            project.compiler.include_dirs.add(include_dir)
            project.compiler.library_dirs.add(library_dir)
            project.compiler.link(Cython.python_library())

        def cython_preprocess(project):
            print('Processing', len(project.cython_sources), 'file(s)')

            out_sources = []

            # TODO: Move this to a file_loop function in Project
            for idx, file in enumerate(project.cython_sources):
                in_file = file.resolve()
                in_file = in_file.relative_to(project.working_dir)

                out_file = Path(project.output_dir, 'cython', in_file)
                out_file = Path(Cython.as_source(out_file))
                out_dir = out_file.parent

                # Create path for output file if it does not exist
                out_dir.mkdir(parents=True, exist_ok=True)

                # Print what's happening
                print_in = str(in_file)
                print_out = str(out_file.relative_to(project.output_dir))
                print('[{0:3.0f}%]'.format((idx+1)/len(project.cython_sources)*100), end=' ')
                Style.object('Processing', in_file, '->', print_out)

                # Fail if one of the files doesn't compile
                if not project.cython.process(str(file), str(out_file)):
                    raise StageFailException(__name__)

                out_sources.append(str(out_file))

            if compile_generated:
                project.sources.add(*out_sources)

        def cython_hook(fn, project):
            def _hook():
                cython_preprocess(project)
                fn()

            return _hook

        try:
            project.hook_stage('preprocess', cython_hook)
        except KeyError:
            # TODO: This is a bullshit limitation
            Style.error('Trying to add Cython to a project with no preprocess stage')
            Style.error('Please add a dummy preprocess stage')
            raise StageFailException(__name__)

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

        Path(out_file).parent.mkdir(parents=True, exist_ok=True)
        args = ['cython'] + arg_settings + [str(in_file), '-o', str(out_file)]

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

    def as_source(self, filename):
        if self.cpp:
            return str(Path(filename))+'.cpp'
        else:
            return str(Path(filename))+'.c'

    @staticmethod
    def find_include_dir(filename="Python.h"):
        import sys

        candidates = [Path(sys.exec_prefix, 'include/'), Path('/include'), Path('/usr/include')]

        for path in candidates:
            if Path(path, filename).exists():
                return str(path)

        return None

    @staticmethod
    def python_library():
        import sys
        major = sys.version_info[0]
        minor = sys.version_info[1]

        return 'python'+str(major)+str(minor)

    @staticmethod
    def python_library_file():

        return platform.current.as_static_library(Cython.python_library())

    @staticmethod
    def find_lib_dir(filename=None):
        import sys

        if filename is None:
            Cython.python_library_file()

        candidates = [Path(sys.exec_prefix, 'libs/'), Path('/lib'), Path('/usr/lib')]

        for path in candidates:
            if Path(path, filename).exists():
                return str(path)

        return None
