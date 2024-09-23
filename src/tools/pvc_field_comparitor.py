import xml.etree.ElementTree as ET
from glob import glob

pvc_file_path = r"C:\_PV\IFAC\PV_Project.xml"
templates_path = r"C:\_PV\forms3"


def get_pvc_names(pvc_export_file):
    tree = ET.parse(pvc_export_file)
    root = tree.getroot()
    result = list()
    for parent in root.findall(".//CaptureIndex_Job"):
        # Find the 'name' element
        name = parent.find('Name').text
        if '[SYSTEM]' not in name:
            result.append(name)
    return result


def get_template_names(template_folder):
    csvs = glob(f'{template_folder}\\*.csv')
    result = list()
    for path in csvs:
        with open(path, 'r') as file:
            while line := file.readline():
                if line:
                    result.append(line.strip())
    return result


if __name__ == '__main__':
    pv_names = get_pvc_names(pvc_file_path)
    tp_names = get_template_names(templates_path)

    for i, pv in enumerate(pv_names):
        idx = pv_names.index(pv)
        tp = tp_names[idx]
        # print(i, pv)
        if pv != tp:
            print('\t', pv, tp)

    print(len(pv_names), len(tp_names))
