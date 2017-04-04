from .style import Style

def run(file, target='build'):
    import importlib
    import importlib.util
    import inspect
    from pathlib import Path

    name = Path(file).name
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        build = getattr(module, target)
    except:
        print(Style.error(name, 'has no {0} attribute!'.format(target)))
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

    return run()
