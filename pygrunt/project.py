class Project:
    def __init__(self):
        self.sources = []
        self.include_dirs = []
        self.linker_flags = []
        self.working_dir = None
        self.output_dir = None

    # For now accept a single parameter and glob
    def add_sources(sources, recursive=False):
        from glob import glob
        self.sources.extend(glob(sources, recursive))
