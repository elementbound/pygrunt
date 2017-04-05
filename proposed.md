# Proposals/plans for pygrunt #

## FileSets ##

> This feature has been added before v0.0.30

These would act pretty much like lists, except a bit more clever and specialized for files. You
can index and iterate them the same way. FileSets store Path objects, have `add` and `remove`
methods to manipulate contents and don't store the same file twice. Also, important, they are
**unordered**.

A variant of this class would be the DirectorySet.

These classes would be used in the Project class to store source files, include- and library
directories.

## Projects ##

> This feature has been added before v0.0.30
> Note: this doesn't include compound projects

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

### Compound Projects ###

If a project produces multiple binaries that may even depend on eachother, a CompoundProject
can be used to combine them. The CompoundProject will try to run through its stages in a smarter
way, for example if two projects share source files, don't compile those twice.

The CompoundProject would maintain an **ordered** list of Projects to run.

### Running pygrunt scripts ###

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

## Platforms ##

Add a platform module, with a base class and separate subclasses for supported platforms. These
platforms would have class methods, firstly to see if the actual platform is the current one.
Other platform-specific functionality could go here as we go on.

The main idea is to replace

``if platform.system() is not 'Windows'``

with

``if not pygrunt.platform.Windows(): ``
