import glob
import xml.etree.ElementTree as ET
import os

class_names = ['red', 'yellow', 'green', 'off', 'wait_on']

def single_xml_to_txt(xml_file, dstDir):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {xml_file}: {e}")
        return

    if not os.path.exists(dstDir):
        os.makedirs(dstDir)

    txt_file_path = os.path.join(dstDir, os.path.basename(xml_file).split('.')[0] + '.' + os.path.basename(xml_file).split('.')[1] + ".txt")
    with open(txt_file_path, 'w') as txt_file:
        for member in root.findall('object'):
            picture_width = int(root.find('size')[0].text)
            picture_height = int(root.find('size')[1].text)
            class_name = member[0].text
            if class_name not in class_names:
                print(f"Class {class_name} not in class_names, skipping...")
                continue
            class_num = class_names.index(class_name)
            box_x_min = int(member[4][0].text)
            box_y_min = int(member[4][1].text)
            box_x_max = int(member[4][2].text)
            box_y_max = int(member[4][3].text)
            x_center = (box_x_min + box_x_max) / (2.0 * picture_width)
            y_center = (box_y_min + box_y_max) / (2.0 * picture_height)
            width = (box_x_max - box_x_min) / picture_width
            height = (box_y_max - box_y_min) / picture_height
            txt_file.write(f"{class_num} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    print(f"Processed {xml_file} -> {txt_file_path}")

def dir_xml_to_txt(path, dstDir):
    if not os.path.exists(path):
        print(f"Source directory {path} does not exist.")
        return
    for xml_file in glob.glob(os.path.join(path, '*.xml')):
        single_xml_to_txt(xml_file, dstDir)

def main(path, dstDir):
    dir_xml_to_txt(path, dstDir)

if __name__ == '__main__':
    srcDir = 'F:\\TrafficLights\\Annotations'
    dstDir = 'F:\\TrafficLights\\train'
    main(srcDir, dstDir)
