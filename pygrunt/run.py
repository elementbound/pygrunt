def run(file):
    import importlib
    import importlib.util
    import inspect
    from pathlib import Path

    name = Path(file).name
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        build = getattr(module, 'build')
    except:
        print(Style.error(name, 'has no build attribute!'))
        return False

    if inspect.isfunction(build):
        return build()

    try:
        run = getattr(build, 'run')
    except:
        print(Style.error('build attribute is (supposedly) a class but has no run method!'))

    return run()
