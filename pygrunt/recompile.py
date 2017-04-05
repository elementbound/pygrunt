class RecompileStrategy:
    def __init__(self, compiler=None):
        self.cache = {}
        self.compiler = compiler

    def checksum(self, file):
        raise NotImplementedError()

    def compare_checksums(self, cached, current):
        raise NotImplementedError()

    def should_recompile(self, file):
        c = self.checksum(file)

        if file not in self.cache:
            self.cache[file] = c
            return True
        else:
            result = self.compare_checksums(self.cache[file], c)
            self.cache[file] = c
            return result

    def save_cache(self, file):
        import json

        with open(file, 'w') as f:
            json.dump(self.cache, f, indent=4, sort_keys=True)

    def load_cache(self, file):
        import json

        try:
            with open(file, 'r') as f:
                self.cache = json.load(f)
        except:
            # Fail silently
            pass

    def clear_cache(self):
        self.cache.clear()


class AlwaysRecompile(RecompileStrategy):
    def checksum(self, file):
        return 0

    def compare_checksums(self, cached, current):
        return True


class PreprocessHash(RecompileStrategy):
    def checksum(self, file):
        import binascii

        preprocess = self.compiler.preprocess_source(file)
        return binascii.crc32(preprocess.encode('utf-8'))

    def compare_checksums(self, cached, current):
        # Recompile if checksums differ
        if cached != current:
            return True
        else:
            return False
