import pygrunt

def main():
    project = pygrunt.Project('glwrap')
    project.working_dir = 'compile-src/glwrap/'
    project.output_dir = 'build/'
    project.type = 'library'
    project.sanitize()

    project.add_sources('*.cpp')
    project.add_sources('mesh/*.cpp')

    project.link('glfw3')
    project.link('gdi32')
    project.link('opengl32')
    project.link('glew32')
    project.link('png')
    project.link('z')

    cc = pygrunt.GCCCompiler(cpp=True)
    cc.optimize('more')
    cc.standard('c++11')
    cc.compile_project(project)

if __name__ == '__main__':
    main()
