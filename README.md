# pygrunt #

pygrunt is a simple build system for C/C++ projects.

Projects are described entirely in Python. Since Python is also an excellent scripting language
with a huge ecosystem built around it, it makes easy to do secondary tasks like checking platform,
conditionally including or excluding source files, filter them based on certain conditions,
move files around on the filesystem or handle command-line parameters.

Since the project is a one-night experiment so far ( *a too long night...* ), it supports only
MinGW ( currently called GCCCompiler, to be fixed in the future ). However, pygrunt is designed
with compiler-independence in mind. It should be relatively easy to add support for other
compilers, given enough knowledge about the compiler itself.

Features are also in short supply, we'll see where this project goes.

## Installing ##

A very early version of ``setup.py`` is included in the repository. Simply run the script and
it will set up pygrunt with all of its dependencies:

``python setup.py install``

If you want to work on the code instead, run

``python setup.py develop``

The setup will create a ``pygrunt`` command that you can call from your console.

> Since the project uses other git repos as examples, you might need to run

> ``git submodule update --init --recursive``

> after cloning.
> This will clone all the submodules so the examples have actual sources to build.

## Usage ##

Projects that build with pygrunt provide a Python script, usually named after the project itself.
An example project, called [GLWrap](https://github.com/elementbound/glwrap) is included in this
repository. Its corresponding script is called ``glwrap.py``.

To build GLWrap, type

``pygrunt examples/glwrap.py``

To build your own project with pygrunt, write a Python script that uses the pygrunt module and
let it do the work. Currently, if all you need is to compile a bunch of source files and link
them together, pygrunt should be fine. See the repo's root directory for examples.
Here's a simple one:

```python
import pygrunt
import pygrunt.compiler

def build():
    # Setup project
    project = pygrunt.Project('hello')
    project.working_dir = 'hello/'
    project.output_dir = 'build/'

    # Sanitize aka. set reasonable defaults
    # Also needed before adding sources
    # ( otherwise pygrunt will be looking in the wrong directories )
    project.sanitize()

    # Add sources
    project.sources.add('*.c')

    # Compile the whole thing
    #project.compiler = pygrunt.compiler.any()
    #project.compile()
    project.compiler = pygrunt.compiler.any()
    project.compile()

```

Output:
```
Looking for GCC on PATH...
Found GCC at D:\dev\compilers\mingw\bin\gcc.exe
Source directory is D:\dev\python\pygrunt\examples\hello
Build directory is D:\dev\python\pygrunt\examples\build
[100%] Compiling hello.c -> hello.o
Linking executable build/hello ...
```

## Dependencies ##

[Colorama](https://pypi.python.org/pypi/colorama) is used for fancy, colored output.

## Name ##

Yes, I'm aware that the name is already in use: [PyGrunt](https://github.com/Mayo-QIN/pygrunt)

The project looks awesome, and also used the name earlier, which means **this project will be renamed
in the future.**

## Todo ##

See the [proposals](proposed.md).

## License ##

pygrunt is licensed under the GNU GPL v3 license. See [LICENSE](LICENSE) for more details.

This license only applies to pygrunt code ( all source files under the pygrunt directory ),
other components with different licenses may be present in the repository ( for example the
compile-src directory ).
