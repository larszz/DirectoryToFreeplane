import os

from lxml import etree


class Helpers:
    class ElementHelper:
        @staticmethod
        def subelements_to_dict(element: etree._Element) -> dict:
            ret = {}
            for c in element:
                ret[c.tag] = c
            return ret

        @staticmethod
        def get_element_from_subelement_dict(subelements: dict, key: str):
            if (subelements is None) | (key is None):
                return None

            if key not in subelements.keys():
                return None

            return subelements[key]




        @staticmethod
        def check_element_attribute_has_value(element: etree._Element, attribute: str, value: str) -> bool:
            # params not set
            if (element is None) | (attribute is None) | (value is None):
                return False

            # attribute not available
            if attribute not in element.attrib:
                return False

            return element.attrib[attribute] == value

        @staticmethod
        def get_index_of_element_attribute_with_value(parent, attribute: str, value: str) -> int:
            if (parent is None) | (attribute is None) | (value is None):
                return -1

            if not etree.iselement(parent):
                return -1

            counter = 0
            for child in parent:
                if Helpers.ElementHelper.check_element_attribute_has_value(child, attribute, value):
                    return counter
                counter += 1

            # not found
            return -1

        @staticmethod
        def check_element_tag_is_value(element: etree._Element, value: str) -> bool:
            # params not set
            if (element is None) | (value is None):
                return False

            return element.tag == value

        @staticmethod
        def get_index_of_element_child_with_tag(parent, value: str) -> int:
            if (parent is None) | (value is None):
                return -1

            if not etree.iselement(parent):
                return -1

            counter = 0
            for child in parent:
                if Helpers.ElementHelper.check_element_tag_is_value(child, value):
                    return counter
                counter += 1

            # not found
            return -1

    class OsHelper:
        @staticmethod
        def file_exist(filepath: str) -> bool:
            if filepath is None:
                return False
            return os.path.isfile(filepath)

        @staticmethod
        def directory_exist(dirpath: str) -> bool:
            if dirpath is None:
                return False
            return os.path.isdir(dirpath)