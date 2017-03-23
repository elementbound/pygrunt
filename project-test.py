import pygrunt

def main():
    project = pygrunt.Project('vecmath')
    project.working_dir = 'compile-src/'
    project.output_dir = 'build/'

    project.define('DEBUG')
    project.flag('Wall')
    project.add_sources('compile-src/vecmath/*.c')

    cc = pygrunt.GCCCompiler()
    cc.optimize('size')
    cc.compile_project(project)

if __name__ == '__main__':
    main()
