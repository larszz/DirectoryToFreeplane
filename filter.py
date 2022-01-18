from conditiontype import ComparisonType
from filtercondition import FilterCondition
from helpers import ElementHelper, BoolHelper, OsHelper
from names import SettingNames
from path import Path


class Filter:

    def __init__(self):
        self.exclude_conditions = []
        self.exclude_paths = []
        self.include_conditions = []
        self.include_paths = []

    def initialize_values(self, exclude_conditions: [], exclude_paths: [], include_conditions: [], include_paths: []):
        self.exclude_conditions = exclude_conditions
        self.exclude_paths = exclude_paths
        self.include_conditions = include_conditions
        self.include_paths = include_paths


    def initialize_filter_conditions_from_elements(self, base_element):
        if base_element is None:
            return
        return # todo continue

    def check_matching_excluding_rules(self, text: str, path: Path = None) -> bool:
        if path is not None:
            if Filter.check_matching_paths(self.exclude_paths, path.absolute):
                return True
        return Filter.check_matching_conditions(self.exclude_conditions, text)
    
    def check_matching_including_rules(self, text: str, path: Path = None) -> bool:
        # if there are including paths defined but path is not part of it, skip this
        # -> no including paths defined means every path is included!
        if path is not None:
            if not Filter.check_matching_paths(self.include_paths, path.absolute, default_on_empty_list=True):
                return False
        return Filter.check_matching_conditions(self.include_conditions, text)

    def check_filter_is_matched(self, text: str, path: Path = None) -> bool:
        if self.check_matching_excluding_rules(text, path):
            return False
        return self.check_matching_including_rules(text, path)

    @staticmethod
    def check_matching_conditions(conditions: [], text: str) -> bool:
        if conditions is None:
            return False
        if text is None:
            return False

        for con in conditions:
            con.check_matching_condition(text)
        return False

    @staticmethod
    def check_matching_paths(lst: [], path: str, default_on_empty_list: bool = False) -> bool:
        if lst is None:
            return False
        if len(lst) <= 0:
            return default_on_empty_list
        if path is None:
            return False
        if len(path) <= 0:
            return False
        for p in lst:
            if p.check_matching_condition(path):
                return True
        return False



    @staticmethod
    def get_filter_conditions_from_element_by_tag(element, filter_tag: str, comparison_type: ComparisonType) -> []:
        condition_list = []
        if element is None:
            return condition_list
        if filter_tag is None:
            return condition_list

        ElementHelper.get_all_subelements(element)
        nodes = ElementHelper.get_all_subelements_with_tag(element, filter_tag)
        for n in nodes:
            condition = FilterCondition.get_filter_condition_from_element(n, comparison_type)
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
        # TODO: alles in eine Liste
        ret_filter.exclude_conditions = Filter.get_filter_conditions_from_element_by_tag(exclude_conditions_element,
                                                                                         SettingNames.Elements.prefix, ComparisonType.PREFIX)
        ret_filter.exclude_suffixes = Filter.get_filter_conditions_from_element_by_tag(exclude_conditions_element,
                                                                                       SettingNames.Elements.suffix, ComparisonType.SUFFIX)
        ret_filter.exclude_contains = Filter.get_filter_conditions_from_element_by_tag(exclude_conditions_element,
                                                                                       SettingNames.Elements.contains, ComparisonType.CONTAINS)
        ret_filter.exclude_paths = Filter.get_filter_conditions_from_element_by_tag(exclude_conditions_element,
                                                                                    SettingNames.Elements.path, ComparisonType.PATH)
        # include conditions
        ret_filter.include_conditions = Filter.get_filter_conditions_from_element_by_tag(include_conditions_element,
                                                                                         SettingNames.Elements.prefix, ComparisonType.PREFIX)
        ret_filter.include_suffixes = Filter.get_filter_conditions_from_element_by_tag(include_conditions_element,
                                                                                       SettingNames.Elements.suffix, ComparisonType.SUFFIX)
        ret_filter.include_contains = Filter.get_filter_conditions_from_element_by_tag(include_conditions_element,
                                                                                       SettingNames.Elements.contains, ComparisonType.CONTAINS)
        ret_filter.include_paths = Filter.get_filter_conditions_from_element_by_tag(include_conditions_element,
                                                                                    SettingNames.Elements.path, ComparisonType.PATH)

        return ret_filter





