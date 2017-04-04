from style import Style

def run(file, target='build'):
    import importlib
    import importlib.util
    import inspect
    from pathlib import Path

    name = Path(file).with_suffix('')
    name = str(name)
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        build = getattr(module, target)
    except:
        print(Style.error('{project} has no {target} attribute!'.format(project=name, target=target)))
        return False

    if inspect.isfunction(build):
        return build()

    if inspect.isclass(build):
        instance = build()
        return instance.run()

    try:
        run = getattr(build, 'run')
    except:
        print(Style.error('build attribute is (supposedly) a class but has no run method!'))
        return False

    return run()

if __name__ == '__main__':
    import sys
    import os

    # Add current path to sys.path so pygrunt can be found
    # TODO: Remove this once pygrunt becomes an actual package
    sys.path.append(os.path.abspath(os.curdir))

    run(*sys.argv[1:])
