import os
from pathlib import Path
from glob import glob

# TODO: Use set instead of list
class FileSet:
    def __init__(self):
        self._data = []
        self.working_directory = Path(os.curdir)

    def _process_str_paths(self, paths):
        # TODO: Dies if a file doesn't exist
        return [Path(file).resolve() for file in paths]

    def _glob(self, pattern):
        return self.working_directory.glob(pattern)

    def add(self, *args):
        added = 0

        for pattern in args:
            files = self._glob(pattern)
            files = self._process_str_paths(files)

            if not files:
                # TODO: Proper handling of this?
                print('Include pattern did not match:', pattern)
            else:
                for file in files:
                    if file not in self._data:
                        self._data.append(file)
                        added += 1

        return added

    def remove(self, *args, recursive=False, cwd=os.curdir):
        removed = 0

        for pattern in args:
            files = self._glob(pattern, recursive, cwd)
            files = self._process_str_paths(files)

            if not files:
                # TODO: Proper handling of this?
                print('Exclude pattern did not match:', pattern)
            else:
                for file in files:
                    if file in self._data:
                        self._data.remove(file)
                        removed += 1

        return removed

    def strings(self):
        return [str(file) for file in self._data]

    def __len__(self):
        return self._data.__len__()

    def __length_hint__(self):
        return self._data.__length_hint__()

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __setitem__(self, key, value):
        # TODO: Are we surely want to let this happen?
        return self._data.__setitem__(key, value)

    def __delitem__(self, key):
        return self._data.__delitem__(key)

    def __iter__(self):
        return self._data.__iter__()

    def __reversed__(self):
        return self._data.__reversed__()

    def __contains__(self, key):
        return self._data.__contains__(key)

    def __str__(self):
        return self._data.__str__()

    def __repr__(self):
        return self._data.__repr__()


class DirectorySet(FileSet):
    def add(self, *args):
        directories = self._process_str_paths(args)
        directories = [directory for directory in directories if directory.is_dir()]

        added = 0
        for directory in directories:
            if directory not in self._data:
                self._data.append(directory)
                added += 1

        return added

    def remove(self, *args):
        directories = self._process_str_paths(args)
        directories = [directory for directory in directories if directory.is_dir()]

        removed = 0
        for directory in directories:
            if directory in self._data:
                self._data.remove(directory)
                removed += 1

        return removed
