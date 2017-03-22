class Project:
    def __init__(self, name):
        self.name = name

        self.sources = []
        self.include_dirs = []
        self.linker_flags = []
        self.working_dir = None
        self.output_dir = None

        self.executable = None

    # For now accept a single parameter and glob
    def add_sources(self, sources, recursive=False):
        from glob import glob
        self.sources.extend(glob(sources, recursive=recursive))

    # Set some sane defaults
    def sanitize(self):
        import os.path

        if not self.working_dir:
            self.working_dir = os.path.curdir

        if not self.output_dir:
            self.output_dir = os.path.join(self.working_dir, 'build', '')

        if not self.executable:
            # TODO: no ugly Windows .exe ending, make it cross-platform-er
            self.executable = os.path.join(self.output_dir, self.name+'.exe')
