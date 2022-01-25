from lxml import etree

import subnodesetting
from filter import Filter
from helpers.helpers import StringHelper, OsHelper
from helpers.xml_helper import XmlHelper as xh

from names import SettingNames
from values import Values
from subnodesetting import SubnodeSetting
import os


class Setting:

    def __init__(self):
        self.output_file_path = Values.SettingValues.outputpath_default
        self.input_directory_path = None
        self.excluded_paths = []
        self.excluded_filetypes = []


    def get_subnode_settings_from_root_node(self, setting_element) -> []:
        if setting_element is None:
            return []

        # get subnodes to add
        subnode_settings = []
        subnodes_to_add = xh.get_first_subelement_with_tag(setting_element, SettingNames.Elements.subnodestoadd)
        if subnodes_to_add is None:
            return subnode_settings

        subnodepackage_list = xh.get_subelements_with_tag(subnodes_to_add, SettingNames.Elements.subnodepackage)
        for snp in subnodepackage_list:
            sn_setting = subnodesetting.SubnodeSetting()
            sn_setting.get_subnode_setting_from_subnode_package(snp)
            if sn_setting is not None:
                subnode_settings.append(sn_setting)


    def init_exclude_settings_from_root_element(self, root_element):
        if root_element is None:
            return None

        exclude_element = xh.get_first_subelement_with_tag(root_element, SettingNames.Elements.exclude)
        if exclude_element is None:
            return

        # add paths from InnerText, seperated by a static set seperator
        exclude_value = xh.get_value_of_element_or_default(exclude_element).strip()
        if (exclude_value is not None) and (exclude_value != ''):
            exclude_rules = (x.strip() for x in exclude_value.split(Values.SettingValues.element_seperator))
            for x in exclude_rules:
                # is filetype (let's see if this works...)
                x_stripped = x.strip()
                if (x_stripped.startswith('.')) & (os.sep not in x_stripped):
                    self.excluded_filetypes.append(StringHelper.remove_quotes_from_string(x_stripped))
                else:
                    self.excluded_paths.append(StringHelper.remove_quotes_from_string(x_stripped))

        # add all found path sub elements
        for rule in xh.get_subelements_with_tag(exclude_element, SettingNames.Elements.path):
            rule_value = xh.get_value_of_element_or_default(rule)
            if rule_value is not None:
                self.excluded_paths.append(rule_value.strip())

        # add excluded filetypes
        for rule in xh.get_subelements_with_tag(exclude_element, SettingNames.Elements.filetype):
            rule_value = xh.get_value_of_element_or_default(rule)
            if rule_value is not None:
                self.excluded_filetypes.append(rule_value.strip())


    def init_from_xml_config_file(self, path: str):
        if path is None:
            return self

        settings_tree = etree.parse(path)
        if settings_tree is None:
            return self

        settings_root = settings_tree.getroot()
        if settings_root is None:
            return self
        return self.init_from_xml_element(settings_root)

    def init_from_xml_element(self, root_element: etree._Element, default_path = None):
        if root_element is None:
            return self
        if default_path is None:
            default_path = os.path.abspath('.')

        # input directory path (-> basepath)
        input_dir_path_element = xh.get_first_subelement_with_tag(root_element, SettingNames.Elements.inputdirpath)
        input_dir_path_value = xh.get_value_of_element_or_default(input_dir_path_element)

        # if input directory is available and valid, it's used as a setting; else current directory is used
        if input_dir_path_value is not None:
            self.input_directory_path = str(StringHelper.remove_quotes_from_string(input_dir_path_element.text).strip())
        else:
            self.input_directory_path = default_path

        # output path
        output_path_value = xh.get_value_of_first_subelement_with_tag_or_default(root_element, SettingNames.Elements.outputfilepath)
        if output_path_value is not None:
            self.output_file_path = StringHelper.remove_quotes_from_string(output_path_value)

        # exclude
        self.init_exclude_settings_from_root_element(root_element)

        subnode_setting_node = xh.get_first_subelement_with_tag(root_element, SettingNames.Elements.subnodestoadd)
        subnode_setting_list = SubnodeSetting.get_multiple_subnode_settings_from_subnodestoadd(subnode_setting_node)

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
    def check_setting_path_valid(self) -> bool:
        if OsHelper.file_exist(self.output_file_path):
            return True
        return False



    def __str__(self):
        return f"SETTING: \n\toutputpath: {self.output_file_path}\n\tinputdirpath: {self.input_directory_path}\n\texcluded paths: {str(self.excluded_paths)}\n\texcluded filetypes: {str(self.excluded_filetypes)}\n========"
