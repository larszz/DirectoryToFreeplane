from lxml import etree

from helpers import *
from names import SettingNames
from values import Values


class Setting:

    def __init__(self):
        self.output_path = Values.SettingValues.outputpath_default
        self.exclude = []

    def parse_from_xml(self, path: str):
        if path is None:
            return

        settings_tree = etree.parse(path)
        if settings_tree is None:
            return

        settings_root = settings_tree.getroot()
        if settings_root is None:
            return

        print(settings_root.tag)
        setting_children = Helpers.ElementHelper.subelements_to_dict(settings_root)
        # search for specific settings

        # output path
        output_path_element = Helpers.ElementHelper. \
            get_element_from_subelement_dict(setting_children, SettingNames.Elements.output_path)
        if output_path_element is not None:
            self.output_path = output_path_element.text

        # exclude
        exclude_element = Helpers.ElementHelper. \
            get_element_from_subelement_dict(setting_children, SettingNames.Elements.exclude)
        if (exclude_element is not None):
            # add paths from InnerText, seperated by a static set seperator
            if (exclude_element.text is not None) & (str(exclude_element.text).strip() != ''):
                self.exclude += [x.strip() for x in str(exclude_element.text). \
                    split(Values.SettingValues.element_seperator)]

            # add all found path subelements
            for c_path in exclude_element:
                if c_path.tag == SettingNames.Elements.path:
                    self.exclude.append(str(c_path.text).strip())

        print(str(self))
