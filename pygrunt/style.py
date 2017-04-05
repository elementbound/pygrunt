import colorama

colorama.init(autoreset=True)

def _merge_args(*args, sep=' ', end='\n', r=False):
    return sep.join([str(arg) for arg in args]) + end

class _prefix:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        prefix = self.fn()
        return prefix+_merge_args(*args, **kwargs)

class _prefix_print:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args, **kwargs):
        prefix = self.fn()

        if 'r' in kwargs and kwargs['r']:
            return prefix+_merge_args(*args, **kwargs)

        print(prefix+_merge_args(*args, **kwargs), end='')


class Style:
    @staticmethod
    @_prefix_print
    def object(*args, sep=' ', end=''):
        return colorama.Fore.GREEN

    @staticmethod
    @_prefix_print
    def link(*args, sep=' ', end=''):
        return colorama.Style.BRIGHT + colorama.Fore.MAGENTA

    @staticmethod
    @_prefix_print
    def error(*args, sep=' ', end=''):
        return colorama.Fore.RED

    @staticmethod
    @_prefix_print
    def warning(*args, sep=' ', end=''):
        return colorama.Fore.YELLOW

    @staticmethod
    @_prefix_print
    def title(*args, sep=' ', end=''):
        return colorama.Style.BRIGHT
