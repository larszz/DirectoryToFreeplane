from helpers.helpers import ElementHelper, BoolHelper
from names import SettingNames


class FilterCondition:

    def __init__(self, value: str, exclude: bool = False):
        self.value = value
        self.exclude = exclude

    @staticmethod
    def get_filter_condition_from_element(element, exclude: bool):
        if element is None:
            return None

        content = element.text
        if content is None:
            return None
        if len(content) <= 0:
            return None
        return FilterCondition(content, exclude)

    @staticmethod
    def check_list_of_conditions_if_a_condition_does_match(conditions: [], text: str) -> bool:
        if conditions is None:
            return False
        if text is None:
            return False




class Filter:

    def __init__(self, exclude_prefixes: [] = [], exclude_suffixes: [] = [], exclude_contains: [] = [], exclude_paths: [] = [],include_prefixes: [] = [], include_suffixes: [] = [], include_contains: [] = [], include_paths: [] = []):
        self.exclude_prefixes = exclude_prefixes
        self.exclude_suffixes = exclude_suffixes
        self.exclude_contains = exclude_contains
        self.exclude_paths = exclude_paths
        self.include_prefixes = include_prefixes
        self.include_suffixes = include_suffixes
        self.include_contains = include_contains
        self.include_paths = include_paths

    def check_matching_excluding_rules(self, text: str) -> bool:
        if Filter.check_matching_prefix(self.exclude_prefixes, text):
            return True
        if Filter.check_matching_suffix(self.exclude_suffixes, text):
            return True
        if Filter.check_contains(self.exclude_contains, text):
            return True
        return False
    
    def check_matching_including_rules(self, text: str) -> bool:
        if Filter.check_matching_prefix(self.include_prefixes, text):
            return True
        if Filter.check_matching_suffix(self.include_suffixes, text):
            return True
        if Filter.check_contains(self.include_contains, text):
            return True
        return False

    def check_text_is_matched(self, text: str, path: str = None) -> bool:
        if self.check_matching_excluding_rules(text):
            return False
        return self.check_matching_including_rules(text)

    @staticmethod
    def check_matching_prefix(lst: [], text: str) -> bool:
        if lst is None:
            return False
        if text is None:
            return False

        for e in lst:
            if text.startswith(e):
                return True
        return False

    @staticmethod
    def check_matching_suffix(lst: [], text: str) -> bool:
        if lst is None:
            return False
        if text is None:
            return False

        for e in lst:
            if text.endswith(e):
                return True
        return False

    @staticmethod
    def check_contains(lst: [], text: str) -> bool:
        if lst is None:
            return False
        if text is None:
            return False
        if len(text) <= 0:
            return False

        for e in lst:
            if e in text:
                return True
        return False

    @staticmethod
    def get_filter_conditions_by_tag(element, filter_tag: str, exclude: bool) -> []:
        condition_list = []
        if element is None:
            return condition_list
        if filter_tag is None:
            return condition_list

        nodes = ElementHelper.get_all_subelements_with_tag(element, filter_tag)
        for n in nodes:
            condition = FilterCondition.get_filter_condition_from_element(n, exclude)
            if condition is not None:
                condition_list.append(condition)

        return condition_list

    @staticmethod
    def get_filter_from_filter_node(element):
        ret_filter = Filter()

        if element is None:
            return ret_filter

        exclude_conditions_element = ElementHelper.get_first_subelement_with_tag(element, SettingNames.Elements.exclude)
        include_conditions_element = ElementHelper.get_first_subelement_with_tag(element, SettingNames.Elements.include)

        # exclude conditions
        ret_filter.exclude_prefixes = Filter.get_filter_conditions_by_tag(exclude_conditions_element,
                                                                          SettingNames.Elements.prefix, exclude=True)
        ret_filter.exclude_suffixes = Filter.get_filter_conditions_by_tag(exclude_conditions_element,
                                                                          SettingNames.Elements.suffix, exclude=True)
        ret_filter.exclude_contains = Filter.get_filter_conditions_by_tag(exclude_conditions_element,
                                                                          SettingNames.Elements.contains, exclude=True)
        ret_filter.exclude_paths = Filter.get_filter_conditions_by_tag(exclude_conditions_element,
                                                                       SettingNames.Elements.path, exclude=True)
        # include conditions
        ret_filter.include_prefixes = Filter.get_filter_conditions_by_tag(include_conditions_element,
                                                                          SettingNames.Elements.prefix, exclude=False)
        ret_filter.include_suffixes = Filter.get_filter_conditions_by_tag(include_conditions_element,
                                                                          SettingNames.Elements.suffix, exclude=False)
        ret_filter.include_contains = Filter.get_filter_conditions_by_tag(include_conditions_element,
                                                                          SettingNames.Elements.contains, exclude=False)
        ret_filter.include_paths = Filter.get_filter_conditions_by_tag(include_conditions_element,
                                                                       SettingNames.Elements.path, exclude=False)

        return ret_filter





