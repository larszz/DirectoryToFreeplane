import os

# import lxml
from lxml import etree
import time

from names import Elements, Attributes
import values


class BoolHelper:
    _true_values = ["true", "1"]
    _false_values = ["false", "0"]
    @staticmethod
    def parse_bool_from_text(text: str) -> bool:
        if text is None:
            return False
        if text.lower() in BoolHelper._true_values:
            return True
        return False

class StringHelper:
    @staticmethod
    def remove_quotes_from_string(text: str) -> str:
        if text is None:
            return ''
        text = text.lstrip("'").rstrip("'")
        text = text.lstrip('"').rstrip('"')
        return text


class TimeHelper:
    @staticmethod
    def get_current_unix_time_in_ms():
        utime = int(round(time.time() * 1000))
        return utime


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
        except etree.XMLSyntaxError:
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
    def get_all_subelements_with_tag(element: etree._Element, tag: str) -> []:
        if element is None:
            return []
        if tag is None:
            return []

        subelements = []
        for c in element:
            if c.tag == tag:
                subelements.append(c)
        return subelements


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
    def get_element_attribute_value(element, attribute: str):
        if element is None:
            return None
        if attribute is None:
            return None
        if attribute not in element.attrib:
            return None
        return element.attrib[attribute]


    @staticmethod
    def check_element_attribute_has_value(element: etree._Element, attribute: str, value: str) -> bool:
        if (element is None) | (attribute is None) | (value is None):
            return False

        attrib_value = ElementHelper.get_element_attribute_value(element, attribute)
        if attrib_value is None:
            return False
        return attrib_value == value



    @staticmethod
    def get_index_of_first_element_by_attribute_with_value(parent, attribute: str, value: str) -> int:
        if (parent is None) | (attribute is None) | (value is None):
            return -1

        if not etree.iselement(parent):
            return -1

        counter = 0
        for child in parent:
            if ElementHelper.check_element_attribute_has_value(child, attribute, value):
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
    def get_index_of_first_subelement_with_tag(parent, value: str) -> int:
        if (parent is None) | (value is None):
            return -1

        if not etree.iselement(parent):
            return -1

        counter = 0
        for child in parent:
            if ElementHelper.check_element_tag_is_value(child, value):
                return counter
            counter += 1

        # not found
        return -1


    @staticmethod
    def add_attribute_to_element_if_missing(element: etree._Element, attribute_tag: str, value: str):
        if element is None:
            return element
        if attribute_tag is None:
            return element
        if value is None:
            return element
        if attribute_tag not in element.attrib.keys():
            element.attrib[attribute_tag] = value
        return element


class MindmapHelper:
    @staticmethod
    def get_subnode_by_text_attrib(element, value: str):
        if element is None:
            return None
        if value is None:
            return None

        index = ElementHelper.get_index_of_first_element_by_attribute_with_value(element, Attributes.text, value)
        if index < 0:
            return None
        return element[index]

    @staticmethod
    def get_text_from_subnode(element):
        if element is None:
            return None
        return ElementHelper.get_element_attribute_value(element, Attributes.text)

    @staticmethod
    def add_necessary_attributes_to_node(element: etree._Element):
        ElementHelper.add_attribute_to_element_if_missing(element, Attributes.position,
                                                          values.Values.MindmapValues.node_position_default)
        ElementHelper.add_attribute_to_element_if_missing(element, Attributes.created,
                                                          str(TimeHelper.get_current_unix_time_in_ms()))
        ElementHelper.add_attribute_to_element_if_missing(element, Attributes.modified,
                                                          str(TimeHelper.get_current_unix_time_in_ms()))

    @staticmethod
    def add_valid_subnode_if_missing_and_return(element, text: str, allow_duplicate: bool = False):
        if element is None:
            return None
        if text is None:
            return None

        if not allow_duplicate:
            subnode = MindmapHelper.get_subnode_by_text_attrib(element, text)
            if subnode is not None:
                return subnode

        new_subnode = etree.Element(Elements.node, attrib={Attributes.text: text})
        MindmapHelper.add_necessary_attributes_to_node(new_subnode)
        element.append(new_subnode)
        return MindmapHelper.get_subnode_by_text_attrib(element, text)


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