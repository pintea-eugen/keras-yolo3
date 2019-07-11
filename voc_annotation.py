import xml.etree.ElementTree as ET
import os
from os import getcwd

sets=['train', 'test']

classes = ["textbox", "button", "radiobutton", "checkbox", "dropdown"]

wd = getcwd()


def convert_annotation(image_id, image_set, list_file):
    in_file = open('%s/voc/%s/%s.xml' % (wd, image_set, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


for image_set in sets:
    image_ids = os.listdir('%s/voc/%s' % (wd, image_set))

    list_file = open('%s/yolo/%s.txt' % (wd, image_set), 'w')
    for image_id in image_ids:
        image_id = image_id[:-4]
        list_file.write('%s/images/%s.jpg' % (wd, image_id))
        convert_annotation(image_id, image_set, list_file)
        list_file.write('\n')
    list_file.close()

