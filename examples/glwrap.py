import pygrunt

class GLWrap(pygrunt.Project):
    def init(self):
        self.working_dir = 'glwrap/'
        self.output_dir = 'build/'
        self.executable = 'build/libglwrap'
        self.type = 'library'
        self.sanitize()

        self.compiler = pygrunt.GCCCompiler(cpp=True)

    def gather(self):
        self.sources.add('*.cpp')
        self.sources.add('mesh/*.cpp')

        # The order of linked libraries is preserved
        # The same does not apply to source files
        self.link('glfw3', 'gdi32', 'opengl32', 'glew32', 'png', 'z')

    def compile(self):
        self.compiler.optimize('more')
        self.compiler.standard('c++11')
        self.compiler.compile_project(self)

build = GLWrap()
