import os
from helpers import OsHelper

class Path:

    def __init__(self):
        self.absolute = None
        self.relative = None
        self.relative_as_list = []

    def initialize_vars(self, absolute = None, relative = None, relative_as_list = []):
        self.absolute = absolute
        self.relative = relative
        self.relative_as_list = relative_as_list

    def initialize_from_path(self, path: str, basepath: str = None):
        if path is None:
            return self

        self.absolute = path
        self.relative = str(path.removeprefix('' if basepath is None else basepath)).lstrip(os.path.sep)
        self.relative_as_list = OsHelper.get_path_as_directory_list(self.relative)

        return self
