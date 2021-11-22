from lxml import etree

from helpers import *
from names import SettingNames
from values import Values
import os


class Setting:

    def __init__(self):
        self.output_path = Values.SettingValues.outputpath_default
        self.excluded_paths = []
        self.excluded_filetypes = []


    def parse_from_xml(self, path: str):
        if path is None:
            return

        settings_tree = etree.parse(path)
        if settings_tree is None:
            return

        settings_root = settings_tree.getroot()
        if settings_root is None:
            return

        setting_children = Helpers.ElementHelper.subelements_to_dict(settings_root)

        # search for specific settings
        # output path
        output_path_element = Helpers.ElementHelper. \
            get_element_from_subelement_dict(setting_children, SettingNames.Elements.outputpath)
        if output_path_element is not None:
            self.output_path = output_path_element.text

        # exclude
        exclude_element = Helpers.ElementHelper. \
            get_element_from_subelement_dict(setting_children, SettingNames.Elements.exclude)
        if (exclude_element is not None):
            # add paths from InnerText, seperated by a static set seperator
            if (exclude_element.text is not None) & (str(exclude_element.text).strip() != ''):
                self.excluded_paths += [x.strip() for x in str(exclude_element.text). \
                    split(Values.SettingValues.element_seperator)]
                for x in str(exclude_element.text).split(Values.SettingValues.element_seperator):
                    # is filetype (let's see if this works...)
                    x_stripped = x.strip()
                    if (x_stripped.startswith('.')) & (os.sep not in x_stripped):
                        self.excluded_filetypes.append(x_stripped)
                    else:
                        self.excluded_paths.append(x_stripped)

            # add all found path sub elements
            for exc_element in exclude_element:
                if exc_element.tag == SettingNames.Elements.path:
                    self.excluded_paths.append(str(exc_element.text).strip())
                if exc_element.tag == SettingNames.Elements.filetype:
                    self.excluded_filetypes.append(str(exc_element.text).strip())

        return self

    """
    Returns if the path is excluded in setting
    """
    def check_path_excluded(self, path: str):
        for ft in self.excluded_filetypes:
            if path.endswith(ft):
                return True

        for exc_path in self.excluded_paths:
            if exc_path in path:
                return True
        return False

    def __str__(self):
        return f"SETTING:: outputpath: {self.output_path}; excluded: {str(self.excluded_paths)}"
