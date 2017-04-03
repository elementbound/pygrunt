# Proposals/plans for pygrunt #

## FileSets ##

These would act pretty much like lists, except a bit more clever and specialized for files. You
can index and iterate them the same way. FileSets store Path objects, have `add` and `remove`
methods to manipulate contents and don't store the same file twice. Also, important, they are
**unordered**.

A variant of this class would be the DirectorySet.

These classes would be used in the Project class to store source files, include- and library
directories. 
