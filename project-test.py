import pygrunt.compiler
import pygrunt.project

def main():
    project = pygrunt.project.Project('vecmath')
    project.add_sources('compile-src/vecmath/*.c')

    cc = pygrunt.compiler.GCCCompiler()
    cc.optimize('size')
    cc.compile_project(project)

if __name__ == '__main__':
    main()
