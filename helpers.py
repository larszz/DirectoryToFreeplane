import os

import lxml
from lxml import etree


class Helpers:

    class ElementHelper:

        @staticmethod
        def get_root_element_from_file_path(filepath: str):
            if filepath is None:
                return None
            if len(filepath) <= 0:
                return None
            if not os.path.isfile(filepath):
                return None
            parsed = None
            try:
                parsed = etree.parse(filepath)
            except lxml.etree.XMLSyntaxError:
                return None
            return parsed.getroot()

        ### Returns the first subelement with the given tag
        @staticmethod
        def get_first_subelement_with_tag(element: etree._Element, tag: str) -> etree._Element:
            if element is None:
                return None
            if tag is None:
                return None
            for c in element:
                if c.tag == tag:
                    return c
            return None


        @staticmethod
        def subelements_to_dict(element: etree._Element) -> dict:
            if element is None:
                return {}
            ret = {}
            for c in element:
                if c.tag in ret:
                    print(f"Key '{c.tag}' already in dict, but needs to be unique!")
                    return {}
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