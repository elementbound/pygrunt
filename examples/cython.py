import pygrunt
import pygrunt.compiler
import shutil
from pygrunt import Style
from pygrunt.extras import Cython
from pathlib import Path

class CythonTest(pygrunt.Project):
    def init(self):
        self.working_dir = 'cython/'
        self.output_dir = 'build/'
        self.type = 'shared'
        self.sanitize()

        self.compiler = pygrunt.compiler.any()

        Cython.add_to(self)

    def gather(self):
        self.cython_sources.add('*.pyx')

    def preprocess(self):
        # Dummy preprocess stage
        pass

    def install(self):
        dst = Cython.as_module(Path(self.output_dir, 'cytest'))
        Style.info(self.executable, '->', dst)
        shutil.move(self.executable, dst)

build = CythonTest
