import pygrunt
import platform

def main():
    project = pygrunt.Project('vecmath')
    project.working_dir = 'compile-src/vecmath/'
    project.output_dir = 'build/'
    project.sanitize()

    project.define('DEBUG')
    project.flag('Wall')
    project.sources.add('*.c')

    if platform.system() is not 'Windows':
        project.link('m')

    cc = pygrunt.GCCCompiler()
    cc.optimize('size')
    cc.compile_project(project)

if __name__ == '__main__':
    main()
