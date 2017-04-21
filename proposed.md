# Proposals/plans for pygrunt #

## FileSets ##

> This feature has been added before v0.0.30

These would act pretty much like lists, except a bit more clever and specialized for files. You
can index and iterate them the same way. FileSets store Path objects, have `add` and `remove`
methods to manipulate contents and don't store the same file twice.

A variant of this class would be the DirectorySet.

These classes would be used in the Project class to store source files, include- and library
directories.

## Projects ##

> This feature has been added before v0.0.30

> Note: this only includes the core feature, not the related features in the next chapters

Instead of writing a function to build the whole project, the Project class could do this
in a smarter way.

Each project would take a bunch of source files and produce a binary. This binary could be either
an executable or a library. Optionally, it could install the resulting binary to the compiler's
appropriate directory.

Projects would have different stages:
 1. **Gather** - add source files and other dependencies  
 2. **Validate** - check dependencies, do other validations
 3. **Preprocess** - configure headers, generate code as necessary
 4. **Compile** - produce binary
 5. **Install** - optional, copy the resulting binary to compiler or to user-supplied location

Each stage corresponds to a function in the Project class. This class would be subclassed by the
user, overriding each stage.

These stages could be overridden or straight up skipped through a more generic BarebonesProject
class.

### Stage hooks ###

> This feature was added in v0.4

Optionally, hooks could be added to the project's stages. These are basically Python's decorators:
they get the stage function and get called instead of the actual stage.

This is an easy way to hook into the gather stage and sanitize, or hook into the compile stage
and load/save the recompile cache as necessary.

### Compound Projects ###

> This feature is planned for v0.6

If a project produces multiple binaries that may even depend on eachother, a CompoundProject
can be used to combine them. The CompoundProject will try to run through its stages in a smarter
way, for example if two projects share source files, don't compile those twice.

The CompoundProject would maintain an **ordered** list of Projects to run.

> Possibly call these **WaterfallProject**

CompoundProjects would be defined in a markup-like manner:

```python
import pygrunt

class FooProject(pygrunt.Project):
	"""Foo project"""

class BarProject(pygrunt.Project):
	"""Bar project"""

class CombinedProject(pygrunt.WaterfallProject):
	projects = [
		FooProject,
		BarProject
	]

build = CombinedProject
```

The projects defined in the class variable can either be Project-like classes ( no explicit
type checking is done ), or instances of those classes, in case you want to customize it
through its constructor.

This way, you can also build a hierarchy of projects. For example, have separate projects for
each library, then each test, group the libraries into one WaterfallProject, the tests into
another, then group these two into a compile-all project which is later defined as *build*.

### Single Project Multiple Output ###

> This feature is planned for v0.6 or v0.7

This can be relevant for many projects. For now, it's especially relevant for Cython projects.

The idea is to have a main project, which will combine all the sources, then the individual
outputs will just link the necessary object files.

These outputs should be described with a simple and concise syntax, either as a class variable
or as a list in the project's init stage. The parent project would combine the common sources,
settings and linked libraries. These would be inherited by its outputs. The outputs themselves
would be defined with the settings specific to that output.

Since I'm still trying to not complicate the hierarchy ( everything is a project, either a
complex or simple ), this would be easily implemented with a Project class, with a special
constructor, so the syntax could be kept concise.

Obviously it would get more verbose if additional customization is needed ( include dirs,
flags, any compiler setting in general ). Compiler settings could possibly be packed into
a utility constructor. Putting these additional settings into the project's constructor would
mean that the output project has to know about the compiler's specifics too.

> What about a builder-like syntax?
```python
output = pygrunt.OutputProject()
	.sources('tests/window.cpp')
	.set_compiler(pygrunt.compiler.any())
	.compiler_config('set_standard', 'c11')
	.compiler_config('link', 'glfw3', 'opengl32')
```
> Although, this would blindly forward function calls, which might not exactly be hack-free.
> Again, we don't want to filter these from the Project's code, because the Project really
> doesn't want to mess with the compiler's specifics ( or any of its external components, for
> that matter ).

> It would also be nice to have an autocomplete-compatible solution, instead of passing
> function names as strings.

## Running pygrunt scripts ##

> This feature has been added before v0.0.30

Not sure how would this be useful, but a runner function might be fun.

The idea is to support simple functions and Project subclasses as well. The runner function would
take a module- or filename, import it and look for a build attribute. If it's a function then
just run it, if it's a variable then see if it's a project and try to run it.

Also add an executable for this runner. So, technically, there would be now two ways to build
a project:

```
py glwrap.py
pygrunt glwrap
```

**Note:** Building projects by simply running the Python scripts is semi-deprecated. Developers
are still free to write their scripts that way, but using the pygrunt command is encouraged.

### Command line arguments ###

> See branch proposal-cmdargs

These would be caught and processed by the Project class. Later on as more arguments get added,
it will probably make more sense that each module catches its own related command-line arguments
and act accordingly. We'll see.

Some useful arguments:
 * --clear: Clear output directory  
 * --clear-cache: Clear recompile cache
 * --expose-options: Print data about project options

## Platforms ##

> This feature was added in 0.2.0

Add a platform module, with a base class and separate subclasses for supported platforms. These
platforms would have class methods, firstly to see if the actual platform is the current one.
Other platform-specific functionality could go here as we go on.

The main idea is to replace

``if platform.system() is not 'Windows'``

with

``if not pygrunt.platform.Windows(): ``

The platform classes would also provide help with file name formatting and other system-specific
operations ( like querying path, or possibly even looking up executables on the system )

## Templating ##

Templating is a bit out of scope for this project. There are other libraries to do that ( see
[Jinja](http://jinja.pocoo.org/) ). These libraries could very well be used in Project's
*preprocess* stage.

However, CMake also has its own 'templating' with its configure step. A simple class could
be added to support porting from CMake.

## Options ##

Also a feature heavily inspired by CMake.

Each project could define several options of various kinds, each with reasonable defaults.
When running the script, a command line argument could be passed to skip the entire options
prompt and just use defaults.

Otherwise, a simple console prompt could be presented to the user to manage settings.

### Integrated or separate UI? ###

Writing a prompt as a GUI application or as a console form is a whole project in itself.
To be able to use external tools to configure, pygrunt needs to expose all the options, their
types and defaults. This could easily be done by a command line switch.

After the actual config step, the options would be saved to a previously agreed-upon location,
so pygrunt can use it in the build step.

The separate UI would also mean that by default pygrunt will not prompt the user for options,
it will use the defaults instead.

## Extras and Utilities module ##

Some nifty features that don't exactly fit anywhere else.

Extras are **not used** internally by pygrunt, they are there for the users. Examples could
include a class for running Cython or a Java compiler class.

Utilities are common abstractions, useful, also used internally by pygrunt.

### Cython ###

> This feature was added in v0.5

Since one of my projects is using Cython right now, why the hell not write some Cython-handy
features.

The main Cython class would be similar to a Compiler, but would not inherit from it.

A nifty feature would also be a @with_cython decorator for Projects. This would add a cython_sources
FileSet, and a Stage Hook to preprocess ( or a preprocess stage if it's not present ). This would
preprocess all the added cython_sources and generate .c files. Optionally it could add these
generated files to the project's sources.

#### CythonProject ####

The @with_cython feature feels clumsy, since the traditional Project and a Cython project work
differently. The usual Project has a bunch of sources and one output. A Cython Project translates
a bunch of .pyx files to .c and compiles each of them **as a separate module**. So it has multiple
outputs.

It makes a lot more sense to have a CythonProject that does the transpiling and compiling,
instead of trying to cram everything into the Project class.

> What about additional sources needed by the .pyx files?

> If the .pyx files depend on a library, that's fine - just tell Cython's compiler to link against
> them.

> If those are source files, either compile them to a library beforehand with a different project.
> Adding this functionality to CythonProject doesn't make that much sense.
