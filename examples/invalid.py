import pygrunt
import pygrunt.compiler

class InvalidProject(pygrunt.Project):
    def init(self):
        self.working_dir = 'invalid/'
        self.compiler = pygrunt.compiler.any()

        self.sanitize()

    def gather(self):
        self.sources.add('*.c')


build = InvalidProject
