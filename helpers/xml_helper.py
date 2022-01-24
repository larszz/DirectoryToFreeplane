import os

from lxml import etree


class XmlHelper:

    @staticmethod
    def get_root_element_from_file_path(filepath: str):
        if filepath is None:
            return None
        if len(filepath) <= 0:
            return None
        if not os.path.isfile(filepath):
            return None

        try:
            root_element_tree = etree.parse(filepath)
        except etree.XMLSyntaxError:
            return None
        return root_element_tree.getroot()

    @staticmethod
    def get_subelements_with_tag(element: etree._Element, tag: str):
        if element is None:
            return None
        if tag is None:
            return None

        iter = element.iterchildren(tag)
        return list(i for i in iter)

    @staticmethod
    def get_first_subelement_with_tag(element: etree._Element, tag: str):
        if element is None:
            return None
        if tag is None:
            return None
        lst = XmlHelper.get_subelements_with_tag(element, tag)
        if (lst is None) | (len(lst) <= 0):
            return None
        return lst[0]

    @staticmethod
    def get_attribute_of_element(element: etree._Element, key: str):
        if element is None:
            return None
        if key is None:
            return None
        return element.get(key)


if __name__ == '__main__':
    path = r'C:\Users\larsz\Projects\DirectoryToFreeplane\testdir\test.xml'
    root = XmlHelper.get_root_element_from_file_path(path)
    se = XmlHelper.get_subelements_with_tag(root, 'outputfilepath')
    y = XmlHelper.get_attribute_of_element(se[0], 'a')
    x = 0
