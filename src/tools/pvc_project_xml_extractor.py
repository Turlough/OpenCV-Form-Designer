"""
Export the project from PaperVision Capture.
Import it here, and extract the field names.
"""
import xml.etree.ElementTree as ET


filename = r"C:\_PV\IFAC\PV_Project.xml"


tree = ET.parse(filename)
root = tree.getroot()
names = root.findall(".//CaptureIndex_Job//Name")
# Exclude system fields
filtered = list(filter(lambda n: '[SYSTEM]' not in n.text, names))

for name in filtered:

    if '[SYSTEM]' not in name.text:
        print(name.text)
print()
print(len(filtered), 'Fields in all, excluding [SYSTEM] fields')
