import colorama

colorama.init(autoreset=True)

class Style:
    @staticmethod
    def _merge_args(*args, sep=' ', end='\n'):
        return sep.join([str(arg) for arg in args]) + end

    @staticmethod
    def object(*args, sep=' ', end=''):
        return colorama.Fore.GREEN + Style._merge_args(*args, sep=sep, end=end)

    @staticmethod
    def link(*args, sep=' ', end=''):
        return colorama.Style.BRIGHT + colorama.Fore.MAGENTA + Style._merge_args(*args, sep=sep, end=end)

    @staticmethod
    def error(*args, sep=' ', end=''):
        return colorama.Fore.RED + Style._merge_args(*args, sep=sep, end=end)

    @staticmethod
    def warning(*args, sep=' ', end=''):
        return colorama.Fore.YELLOW + Style._merge_args(*args, sep=sep, end=end)

    @staticmethod
    def title(*args, sep=' ', end=''):
        return colorama.Style.BRIGHT + Style._merge_args(*args, sep=sep, end=end)
