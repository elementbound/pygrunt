import pygrunt
import pygrunt.compiler

class PCMtoWAV(pygrunt.Project):
    def init(self):
        self.name = 'pcm-to-wav'

        self.working_dir = 'pcm-to-wav/'
        self.output_dir = 'build/'
        self.sanitize()

    def gather(self):
        self.sources.add('*.c')

        # M_PI is not defined in standard, so also define that
        # TODO: check from compiler if it needs to be defined 
        self.define('M_PI', '3.14159265358979323846264338327950288')

    def compile(self):
        cc = pygrunt.compiler.any()
        cc.standard('c11')
        cc.optimize('more')
        cc.compile_project(self)

build = PCMtoWAV
