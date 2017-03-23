import pygrunt

def main():
    project = pygrunt.Project('glwrap')
    project.working_dir = 'compile-src/glwrap/'
    project.output_dir = 'build/'
    project.type = 'library'
    project.sanitize()

    project.add_sources('*.cpp')
    project.add_sources('mesh/*.cpp')

    # The order of linked libraries is preserved
    # The same does not apply to source files
    project.link('glfw3', 'gdi32', 'opengl32', 'glew32', 'png', 'z')

    cc = pygrunt.GCCCompiler(cpp=True)
    cc.optimize('more')
    cc.standard('c++11')
    cc.compile_project(project)

if __name__ == '__main__':
    main()
