import os
from pathlib import Path
from glob import glob

class FileSet:
    def __init__(self):
        self._data = []

    def _process_str_paths(self, paths):
        return [Path(file).resolve() for file in paths]

    def _glob(pattern, recursive, cwd):
        cwd = Path(cwd)
        return cwd.glob(pattern, recursive=recursive)

    def add(self, *args, recursive=False, cwd=os.curdir):
        added = 0

        for pattern in args:
            files = self._glob(pattern, recursive, cwd)
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
