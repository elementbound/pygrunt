# pygrunt #

pygrunt is a simple build system for C/C++ projects.

Projects are described entirely in Python. Since Python is also an excellent scripting language
with a huge ecosystem built around it, it makes easy to do secondary tasks like checking platform,
conditionally including or excluding source files, filter them based on certain conditions,
move files around on the filesystem or handle command-line parameters.

Since the project is a one-night experiment so far ( *a too long night...* ), it supports only
MinGW ( currently called GCCCompiler, to be fixed in the future ) on Windows ( sloppy
slash-handling ). However, pygrunt is designed compiler-independence in mind. It should
be relatively easy to add support for other compilers, given enough knowledge about the compiler
itself.

Features are also in short supply, we'll see where this project goes.

## Usage ##

Write a Python script that uses the pygrunt module and let it do the work. Currently, if all
you need is to compile a bunch of source files and link them together, pygrunt should be fine.
See the repo's root directory for examples; here's both of them anyhow:

A simple project with a few C files:

```python
import pygrunt

def main():
    project = pygrunt.Project('vecmath')
    project.working_dir = 'compile-src/'
    project.output_dir = 'build/'

    project.define('DEBUG')
    project.flag('Wall')
    project.add_sources('vecmath/*.c')

    cc = pygrunt.GCCCompiler()
    cc.optimize('size')
    cc.compile_project(project)

if __name__ == '__main__':
    main()

```

[GLwrap](https://github.com/elementbound/glwrap) compiled with pygrunt instead of CMake:

```python
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
```
