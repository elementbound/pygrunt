import pygrunt
import pygrunt.compiler
import pygrunt.platform

def build():
    project = pygrunt.Project('vecmath')
    project.working_dir = 'vecmath/'
    project.output_dir = 'build/'
    project.sanitize()

    project.define('DEBUG')
    project.flag('Wall')
    project.sources.add('*.c')

    if not pygrunt.platform.Windows():
        project.link('m')

    cc = pygrunt.compiler.any()
    cc.optimize('size')
    cc.compile_project(project)
