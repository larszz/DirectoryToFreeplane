from conditiontype import ComparisonType


class FilterCondition:
    def __init__(self, value: str, comparison_type: ComparisonType):
        self.value = value
        self.comparison_type = comparison_type

    @staticmethod
    def get_filter_condition_from_element(element, comparison_type: ComparisonType):
        if element is None:
            return None

        content = element.text
        if content is None:
            return None
        if len(content) <= 0:
            return None
        return FilterCondition(content, comparison_type)

    # TODO: hierher Definition des ConditionType umziehen (Prefix, Suffix, Contains, Path)


class PrefixCondition(FilterCondition):
    def __init__(self, value):
        super().__init__(value, ComparisonType.PREFIX)

    def check_matching_condition(self, text: str) -> bool:
        if text is None:
            return False
        return text.startswith(self.value)


class SuffixCondition(FilterCondition):
    def __init__(self, value):
        super().__init__(value, ComparisonType.SUFFIX)

    def check_matching_condition(self, text: str) -> bool:
        if text is None:
            return False
        return text.endswith(self.value)


class ContainsCondition(FilterCondition):
    def __init__(self, value):
        super().__init__(value, ComparisonType.CONTAINS)

    def check_matching_condition(self, text: str) -> bool:
        if text is None:
            return False
        if len(text) <= 0:
            return False
        return self.value in text


class PathCondition(FilterCondition):
    def __init__(self, value):
        super().__init__(value, ComparisonType.PATH)

    def check_matching_condition(self, path: str) -> bool:
        if path is None:
            return False
        return OsHelper.check_path_is_subpath(path, self.value)
