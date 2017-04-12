import pygrunt
import pygrunt.compiler
from pygrunt import Style
import shutil
from pygrunt.extras import Cython

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
        Style.info(self.executable, '->', Cython.as_module(self.executable))
        shutil.move(self.executable, Cython.as_module(self.executable))

build = CythonTest
