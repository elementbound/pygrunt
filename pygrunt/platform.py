import os
from pathlib import Path

class Platform:
    vagueness = 32768

    def __init__(self):
        self._bool = self.__class__.check()

    def __bool__(self):
        return self._bool

    @staticmethod
    def check():
        return False

    @staticmethod
    def as_executable(file):
        raise NotImplementedError()

    @staticmethod
    def as_static_library(file):
        raise NotImplementedError()

    @staticmethod
    def as_shared_library(file):
        raise NotImplementedError()

    @staticmethod
    def path():
        return os.environ['PATH'].split(os.pathsep)

class Unknown(Platform):
    pass

class Windows(Platform):
    vagueness = 0

    def check():
        import platform
        return platform.system() == 'Windows'

    def as_executable(file):
        p = Path(file)
        return str(p.with_suffix('.exe'))

    def as_static_library(file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.a'))

    def as_shared_library(file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.dll'))

# NOTE: I might be wrong on these, needs some actual testing
class Linux(Platform):
    vagueness = 4

    def check():
        import platform
        return platform.system() == 'Linux'

    def as_executable(file):
        p = Path(file)
        return str(p.with_suffix(''))

    def as_static_library(file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.a'))

    def as_shared_library(file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.so'))

def find_current():
    known_platforms = [Windows, Linux]
    best_match = Unknown

    for platform in known_platforms:
        if platform():
            if platform.vagueness < best_match.vagueness:
                best_match = platform

    return best_match

current = find_current()
