import pygrunt

class GLWrap(pygrunt.Project):
    def init(self):
        self.working_dir = 'compile-src/glwrap/'
        self.output_dir = 'build/'
        self.type = 'library'
        self.sanitize()

        self.cc = pygrunt.GCCCompiler(cpp=True)

    def gather(self):
        self.sources.add('*.cpp')
        self.sources.add('mesh/*.cpp')

        # The order of linked libraries is preserved
        # The same does not apply to source files
        self.link('glfw3', 'gdi32', 'opengl32', 'glew32', 'png', 'z')

    def compile(self):
        self.cc.optimize('more')
        self.cc.standard('c++11')
        self.cc.compile_project(self)

build = GLWrap()

if __name__ == '__main__':
    build.run()
