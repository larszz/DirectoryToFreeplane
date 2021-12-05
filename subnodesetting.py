from filter import Filter
from helpers import ElementHelper, MindmapHelper
from names import SettingNames


class SubnodeSetting:

    def __init__(self, subnode_texts: [], filter: Filter):
        self.subnode_texts = subnode_texts
        self.filter = filter

    def add_subnodes_to_element(self, element):
        if element is None:
            return None

        for t in self.subnode_texts:
            MindmapHelper.add_valid_subnode_if_missing_and_return(element, t)
        return element

    def check_node_matches_filter(self, element) -> bool:
        if element is None:
            return False
        if self.filter is None:
            return False

        node_content = MindmapHelper.get_text_from_subnode(element)
        return self.filter.check_text_is_matched(node_content)

    @staticmethod
    def get_list_of_contents_from_element_list(element_list: []) -> []:
        if element_list is None:
            return []
        contents = []
        for e in element_list:
            contents.append(e.text)
        return contents

    @staticmethod
    def get_subnode_setting_from_subnode_package(element):
        if element is None:
            return None

        text_element_list = ElementHelper.get_all_subelements_with_tag(element, SettingNames.Elements.text)
        text_list = SubnodeSetting.get_list_of_contents_from_element_list(text_element_list)

        filter_element = ElementHelper.get_first_subelement_with_tag(element, SettingNames.Elements.filter)
        text_filter = Filter.get_filter_from_filter_node(filter_element)

        return SubnodeSetting(text_list, text_filter)

    @staticmethod
    def get_multiple_subnode_settings_from_subnodestoadd(element):
        subnode_setting_list = []

        if element is None:
            return subnode_setting_list

        packages = ElementHelper.get_all_subelements_with_tag(element, SettingNames.Elements.subnodepackage)
        for p in packages:
            subnode_setting = SubnodeSetting.get_subnode_setting_from_subnode_package(p)
            if subnode_setting is not None:
                subnode_setting_list.append(subnode_setting)
        return subnode_setting_list

