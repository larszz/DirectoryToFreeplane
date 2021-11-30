from helpers import ElementHelper, BoolHelper
from names import SettingNames


class FilterCondition:

    def __init__(self, value: str, negate: bool = False):
        self.value = value
        self.negate = negate

    @staticmethod
    def get_filter_condition_from_element(element):
        if element is None:
            return None
        # text
        content = element.text
        # negate
        negate = False
        negate_text = ElementHelper.get_element_attribute_value(element, SettingNames.Attributes.negate)
        if negate_text is not None:
            negate = BoolHelper.parse_bool_from_text(negate_text)

        return FilterCondition(content, negate)




class Filter:

    def __init__(self, prefixes: [] = [], suffixes: [] = [], contains: [] = [], exclude_paths: [] = []):
        self.prefixes = prefixes
        self.suffixes = suffixes
        self.contains = contains
        self.exclude_paths = exclude_paths

    @staticmethod
    def get_filter_conditions_by_tag(element, filter_tag: str) -> []:
        condition_list = []
        if element is None:
            return condition_list
        if filter_tag is None:
            return condition_list

        nodes = ElementHelper.get_all_subelements_with_tag(element, filter_tag)
        for n in nodes:
            condition = FilterCondition.get_filter_condition_from_element(n)
            if condition is not None:
                condition_list.append(condition)

        return condition_list

    @staticmethod
    def get_filter_from_filter_node(element):
        ret_filter = Filter()

        if element is None:
            return ret_filter

        ret_filter.prefixes = Filter.get_filter_conditions_by_tag(element, SettingNames.Elements.prefix)
        ret_filter.suffixes = Filter.get_filter_conditions_by_tag(element, SettingNames.Elements.suffix)
        ret_filter.contains = Filter.get_filter_conditions_by_tag(element, SettingNames.Elements.contains)
        ret_filter.exclude_paths = Filter.get_filter_conditions_by_tag(element, SettingNames.Elements.excludepath)

        return ret_filter





