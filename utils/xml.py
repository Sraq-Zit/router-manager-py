import xml.etree.ElementTree as ET


def merge_xml(xml1, xml2):
    """
    Merges two XML files with the same root.

    Args:
        xml_file1 (str): The string of the first XML.
        xml_file2 (str): The string of the second XML.

    Returns:
        str: The merged XML string.
    """
    
    root1 = ET.fromstring(xml1)
    root2 = ET.fromstring(xml2)

    # Merge the root elements
    merged_root = merge_elements(root1, root2)

    # Create a new XML tree with the merged root
    merged_tree = ET.ElementTree(merged_root)

    # Convert the merged XML tree to a string
    merged_xml = ET.tostring(merged_tree.getroot(), encoding="utf-8")

    return merged_xml


def merge_elements(element1, element2):
    """
    Recursively merges two XML elements.

    Args:
        element1 (Element): The first XML element.
        element2 (Element): The second XML element.

    Returns:
        Element: The merged XML element.
    """
    merged_element = ET.Element(element1.tag)

    # Merge the attributes of the elements
    merged_element.attrib = {**element1.attrib, **element2.attrib}

    # Merge the children elements
    merged_children = []
    for child1 in element1:
        found = False
        for child2 in element2:
            if child1.tag == child2.tag:
                merged_child = merge_elements(child1, child2)
                merged_children.append(merged_child)
                found = True
                break
        if not found:
            merged_children.append(child1)

    # Append the remaining children of element2
    for child2 in element2:
        found = False
        for child1 in element1:
            if child1.tag == child2.tag:
                found = True
                break
        if not found:
            merged_children.append(child2)

    merged_element.extend(merged_children)
    return merged_element