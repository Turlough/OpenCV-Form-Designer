"""
Export the project from PaperVision Capture.
Import it here, and extract the field names.
"""
import xml.etree.ElementTree as ET


filename = r"C:\_PV\IFAC\PV_Project.xml"


tree = ET.parse(filename)
root = tree.getroot()


# Iterate through all 'parent' elements
for parent in root.findall(".//CaptureIndex_Job"):
    # Find the 'name' element
    name_element = parent.find('Name')
    if '[SYSTEM]' in name_element.text:
        continue
    print(name_element.text)

    values_element = parent.find('PredefinedIndexValues')
    if values_element is not None and list(values_element):
        # If 'values' element is non-empty, print each value with a tab
        for value in values_element.findall('string'):
            print(f"\t{value.text}")

# Exclude system fields
names = root.findall(".//CaptureIndex_Job//Name")
filtered = list(filter(lambda n: '[SYSTEM]' not in n.text, names))
print()
print(len(filtered), 'Fields in all, excluding [SYSTEM] fields')
