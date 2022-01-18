from enum import Enum


class ComparisonType(Enum):
    PREFIX = 1
    SUFFIX = 2
    CONTAINS = 3
    PATH = 4