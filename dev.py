import os
import sys
import argparse
import time

import lxml.etree
from lxml import etree
from io import StringIO

import names
import values
from helpers import ElementHelper, MindmapHelper

from names import Attributes
from setting import Setting

r"""
Tutorial: https://lxml.de/tutorial.html
"""


dirs_to_exclude = [r"\Programme"]

class Directory:

    def __init__(self, dirpath):
        self.dirname = os.path.split(dirpath)[1]
        self.dirpath = dirpath
        self.dirs = []  # list[Directory]
        self.files = []  # list[str]



def xml_test():
    xmlpath = r".\TestFiles\MindMap01.mm"

    tree = etree.parse(xmlpath)

    root = tree.getroot()
    
    testpath = r"Root\parent\child\child2\hippo"
    testpath = os.path.normpath(testpath)
    dirlist = testpath.split(os.sep)

    rec_add_dirs_from_path_and_get_element(root, dirlist)

    result_xml = str(etree.tostring(root, encoding='unicode', pretty_print=True))
    with open(r"TestFiles/MindMap01_result.mm", "w") as h:
        h.write(result_xml)


def dir_test():
    basepath = r"C:\Users\larsz\Documents\Studium\Augsburg\Semester\1. Semester"
    dirpath = basepath

    print("\n" * 5)
    iter = 0
    for (dirpath, dirnames, filenames) in os.walk(dirpath):
        print("\nIter: " + str(iter))
        iter += 1
        print("dirpath:   " + str(dirpath))
        print("dirpath short: " + str(dirpath.split(basepath)))
        print("dirnames:  " + str(dirnames))
        print("filenames: " + str(filenames))

    pass


def path_split_test():
    basepath = r"C:\Users\larsz\Documents\Studium\Augsburg\Semester\1. Semester"

    prefix = r"C:\Users\larsz\Documents\Studium"

    to_work = basepath.lstrip(prefix)

    print(to_work)



def init_rec_print_children(element, maxiter):
    rec_print_children(element, 0, maxiter)


def rec_print_children(element, iter: int, maxiter: int):
    if (maxiter < 0) & (iter > maxiter):
        return

    print("Element: " + str(element.tag))

    for child in element:
        if Attributes.text in child.attrib:
            text = child.attrib[Attributes.text]
        else:
            text = None

        print("* " * iter + "%s (%s)" % (child.tag, text))
        # print("* " * iter + "%s " % (element.keys()))
        rec_print_children(child, iter + 1, maxiter)



# ----------------------------------------------------------
# ----------------------------------------------------------


def rec_add_dirs_from_path_and_get_element(element, path: []):
    if (path is None) | len(path) == 0:
        return element

    cur = str(path[0])

    current_folder_xml_index = ElementHelper.get_index_of_element_attribute_with_value(element,
                                                                                               names.Attributes.text,
                                                                                               cur)

    # if current checked folder does not exist as an element, add the element
    if current_folder_xml_index < 0:

        new_element = etree.Element(names.Elements.node, attrib={Attributes.text: cur})
        MindmapHelper.add_necessary_attributes_to_node(new_element)
        element.append(new_element)
        current_folder_xml_index = ElementHelper.get_index_of_element_attribute_with_value(element,
                                                                                                   names.Attributes.text,
                                                                                                   cur)
    else:
        existing_element = None
    # walk to next level
    path.pop(0)
    return rec_add_dirs_from_path_and_get_element(element[current_folder_xml_index], path)


"""
Returns the path as a list of directories
"""
def get_path_as_directory_list(path: str) -> list:
    if (path is None) | (len(path) <= 0):
        return []
    return os.path.normpath(path).split(os.sep)


def write_string_to_file(filepath: str, output: str):
    if filepath is None:
        return False
    if output is None:
        return False
    with open(filepath, 'wb') as f:
        f.write(output)


def write_mindmap_file_to_path(filepath: str, output: str):
    if filepath is None:
        return False
    if output is None:
        return False
    output = values.Values.MindmapValues.file_prefix + output + values.Values.MindmapValues.file_suffix
    write_string_to_file(filepath, output)

"""
Writes all passed paths to the output XML
"""
def write_paths_to_xml(setting: Setting, file_paths: []):
    # param check
    if setting is None:
        return
    if file_paths is None:
        return
    if len(file_paths) <= 0:
        return

    # logic
    root = ElementHelper.get_root_element_from_file_path(setting.output_file_path)
    if root is None:
        print(f"ERROR: Root element not found!")
        return

    base_node = ElementHelper.get_first_subelement_with_tag(root, names.Elements.node)

    # TODO: change after tests
    setting.output_file_path = r"C:\Users\larsz\Projects\DirectoryToFreeplane\TestFiles\MindMap01_result.mm"

    for p in file_paths:
        file_path_as_list = get_path_as_directory_list(p)
        element = rec_add_dirs_from_path_and_get_element(base_node, file_path_as_list)
        MindmapHelper.add_necessary_attributes_to_node(element)


    etree.indent(base_node)
    output = etree.tostring(base_node, pretty_print=True)
    write_mindmap_file_to_path(setting.output_file_path, output)



"""
Get valid paths of all files under the given base path
"""
def get_valid_filepaths_under_basepath(setting: Setting):
    dirpath = setting.input_directory_path

    file_paths = []
    for (dirpath, dirnames, filenames) in os.walk(dirpath):
        for fn in filenames:
            short_path = str(dirpath.removeprefix(setting.input_directory_path))
            file_path = os.path.join(short_path, fn)
            if setting.check_filepath_excluded(file_path):
                continue
            file_path = file_path.lstrip(os.path.sep)
            file_paths.append(file_path)
    return file_paths


if __name__ == '__main__':
    # parse arguments
    """
    HELP:
    https://docs.python.org/3/library/argparse.html#usage
    https://realpython.com/command-line-interfaces-python-argparse/
    """
    arg_parser = argparse.ArgumentParser(description='Generate a MindMap as an overview for the contents of a folder')
    arg_parser.add_argument('-s', '--settingspath', help='Path to settings file', default='.', )
    arg_parser.add_argument('-o', '--outputpath', help='Output path for the mindmap file to use', default='.', )
    arg_parser.add_argument('-i', '--interactive', help='Allows interactive execution (TO IMPLEMENT)', action='store_true')
    arg_parser.print_help()
    arguments = arg_parser.parse_args()


    # settings path
    settings_path = arguments.settingspath.strip("'")

    setting = Setting().parse_from_xml_config_file(settings_path)
    if not setting.check_setting_path_valid():
        print(f"Setting path not valid!")
        exit(1)
    print()

    # get files to
    paths = get_valid_filepaths_under_basepath(setting)
    write_paths_to_xml(setting, paths)