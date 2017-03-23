import pygrunt

def main():
    project = pygrunt.Project('glwrap')
    project.working_dir = 'compile-src/glwrap/'
    project.output_dir = 'build/'
    project.sanitize()

    project.add_sources('*.cpp')
    project.add_sources('mesh/*.cpp')

    cc = pygrunt.GCCCompiler()
    cc.optimize('more')
    cc.standard('c++11')
    cc.output_type('library')
    cc.compile_project(project)

if __name__ == '__main__':
    main()
