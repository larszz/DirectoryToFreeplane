from lxml import etree

from helpers import *
from names import SettingNames
from values import Values
import os


class Setting:

    def __init__(self):
        self.output_file_path = Values.SettingValues.outputpath_default
        self.input_directory_path = None
        self.excluded_paths = []
        self.excluded_filetypes = []


    def parse_from_xml_config_file(self, path: str):
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
        # input directory path (-> basepath)
        input_dir_path_element = Helpers.ElementHelper.\
            get_element_from_subelement_dict(setting_children, SettingNames.Elements.inputdirpath)
        # if input directory is available and valid, it's used as a setting
        if (input_dir_path_element is not None) \
                & (input_dir_path_element.text is not None) \
                & (input_dir_path_element.text != ''):
            self.input_directory_path = str(input_dir_path_element.text).strip()
        else:
            # else current directory is used
            self.input_directory_path = os.path.dirname(os.path.abspath(path))

        # output path
        output_path_element = Helpers.ElementHelper. \
            get_element_from_subelement_dict(setting_children, SettingNames.Elements.outputfilepath)
        if output_path_element is not None:
            self.output_file_path = output_path_element.text

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
    def check_filepath_excluded(self, path: str):
        for ft in self.excluded_filetypes:
            if path.endswith(ft):
                return True

        for exc_path in self.excluded_paths:
            if exc_path in path:
                return True
        return False

    """
    Checks whether the set paths are pointing to valid locations
    """
    def check_setting_paths_valid(self) -> bool:
        if not Helpers.OsHelper.file_exist(self.output_file_path):
            return False
        if not Helpers.OsHelper.directory_exist(self.input_directory_path):
            return False
        return True



    def __str__(self):
        return f"SETTING: \n\toutputpath: {self.output_file_path}\n\tinputdirpath: {self.input_directory_path}\n\texcluded paths: {str(self.excluded_paths)}\n\texcluded filetypes: {str(self.excluded_filetypes)}\n========"
