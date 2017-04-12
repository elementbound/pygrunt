import os
from pathlib import Path

class Platform:
    vagueness = 32768

    def __init__(self):
        self._bool = self.__class__.check()

    def __bool__(self):
        return self._bool

    @classmethod
    def check(klass):
        return False

    @classmethod
    def as_executable(klass, file):
        raise NotImplementedError()

    @classmethod
    def as_static_library(klass, file):
        raise NotImplementedError()

    @classmethod
    def as_shared_library(klass, file):
        raise NotImplementedError()

    @classmethod
    def as_object(klass, file):
        return str(Path(file).with_suffix('.o'))

    @classmethod
    def path(klass):
        return os.environ['PATH'].split(os.pathsep)

    @classmethod
    def find_executable(klass, name):
        name = klass.as_executable(name)

        for path in klass.path():
            path = Path(path, name)
            if path.is_file():
                return str(path)

        return None

class Unknown(Platform):
    pass

class Windows(Platform):
    vagueness = 0

    @classmethod
    def check(klass):
        import platform
        return platform.system() == 'Windows'

    @classmethod
    def as_executable(klass, file):
        p = Path(file)
        return str(p.with_suffix('.exe'))

    @classmethod
    def as_static_library(klass, file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.a'))

    @classmethod
    def as_shared_library(klass, file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.dll'))

# NOTE: I might be wrong on these, needs some actual testing
class Linux(Platform):
    vagueness = 4

    @classmethod
    def check(klass):
        import platform
        return platform.system() == 'Linux'

    @classmethod
    def as_executable(klass, file):
        p = Path(file)
        return str(p.with_suffix(''))

    @classmethod
    def as_static_library(klass, file):
        p = Path(file)
        if not p.name.startswith('lib'):
            p = p.with_name('lib' + p.name.lower())

        return str(p.with_suffix('.a'))

    @classmethod
    def as_shared_library(klass, file):
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
