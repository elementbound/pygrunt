import pygrunt
import pygrunt.compiler
import pygrunt.platform

def build():
    project = pygrunt.Project('vecmath')
    project.working_dir = 'vecmath/'
    project.output_dir = 'build/'
    project.sanitize()

    cc = project.compiler = pygrunt.compiler.any()

    project.sources.add('*.c')
    cc.define('DEBUG')
    cc.flag('Wall')
    cc.optimize('size')

    if not pygrunt.platform.Windows():
        cc.link('m')

    project.compile()
