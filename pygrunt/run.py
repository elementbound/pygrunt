from pygrunt.style import Style
from pygrunt.version import version
import argparse

def _parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('script', help='Script to run')
    parser.add_argument('target', nargs='?', default='build')

    parser.add_argument('--version', action='store_true', help='Print version info and exit')
    parser.add_argument('--clear', action='store_true', help='Clear output directory')
    parser.add_argument('--clear-cache', action='store_true', help='Clear cache before compiling')

    # TODO: Make target '*' instead of '?' so multiple targets could be ran from the same command

    return parser.parse_args(args)

import sys
args = _parse_args(sys.argv[1:])

def run():
    import importlib
    import importlib.util
    import inspect
    import sys
    import os
    from pathlib import Path

    if args.version:
        print('pygrunt version', version)
        return True

    Style.title('pygrunt version', version)

    file = args.script
    target = args.target

    # Import file
    path = Path(file)

    while True:
        if path.is_file():
            break

        path = path.with_suffix('.py')
        if path.is_file():
            file = str(path)
            break

        Style.error(path, "is not a file!")
        return False

    name = Path(file).with_suffix('')
    name = str(name)
    spec = importlib.util.spec_from_file_location(name, file)

    if spec is None:
        Style.error('Failed to load script; spec is empty')
        Style.error('Module name:', name)
        Style.error('File:', file)
        return False

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Set working directory to file's parent
    os.chdir(str(path.parent))

    # Try to find and run a project
    try:
        build = getattr(module, target)
    except:
        Style.error('{project} has no {target} attribute!'.format(project=name, target=target))
        return False

    if inspect.isfunction(build):
        return build()

    if inspect.isclass(build):
        instance = build()
        return instance.run()

    try:
        run = getattr(build, 'run')
    except:
        Style.error('build attribute is (supposedly) a class but has no run method!')
        return False

    return run()
