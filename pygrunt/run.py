from pygrunt.style import Style

def run():
    import importlib
    import importlib.util
    import inspect
    import sys
    from pathlib import Path

    # Parse command line arguments
    if len(sys.argv) < 2:
        my_name = Path(sys.argv[0]).name
        print('Usage:', my_name, 'file', '[target=build]')
        return False

    file = sys.argv[1]

    target = 'build' if len(sys.argv) < 3 else sys.argv[2]

    # Import file
    path = Path(file)
    if not path.is_file():
        print(Style.error(path, "is not a file!"))
        return False

    name = Path(file).with_suffix('')
    name = str(name)
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Try to find and run a project
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
