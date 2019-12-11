from predict_AI import LINC_detector 
import os
import re
import xml.etree.ElementTree as xTree
from xml.dom import minidom



classes = {
        "1":"cv-dl",
        "2":"cv-dr",
        "3":"cv-f",
        "4":"cv-sl",
        "5":"cv-sr",
        "6":"ear-dl-l",
        "7":"ear-dl-r",
        "8":"ear-dr-l",
        "9":"ear-dr-r",
        "10":"ear-fl",
        "11":"ear-fr",
        "12":"ear-sl",
        "13":"ear-sr",
        "14":"eye-dl-l",
        "15":"eye-dl-r",
        "16":"eye-dr-l",
        "17":"eye-dr-r",
        "18":"eye-fl",
        "19":"eye-fr",
        "20":"eye-sl",
        "21":"eye-sr",
        "22":"nose-dl",
        "23":"nose-dr",
        "24":"nose-f",
        "25":"nose-sl",
        "26":"nose-sr",
        "27":"whisker-dl",
        "28":"whisker-dr",
        "29":"whisker-f",
        "30":"whisker-sl",
        "31":"whisker-sr",
    }

def create_voc(results, path):
    # Create file name for voc
    ann = results   # Annotations dict
    head, tail = os.path.split(path)
    voc_name = re.sub(r'\..*$','.xml',tail)
    voc_path = os.path.join(head, voc_name)

    # Start xml encoding
    root = xTree.Element("annotation")
    folder = xTree.SubElement(root,'folder')
    the_folder = os.path.dirname(ann['path'])
    folder.text = the_folder
    
    # Add metadata
    name = xTree.SubElement(root,'filename')
    name.text = ann['name']
    # Path
    path = xTree.SubElement(root,'path')
    path.text = ann['path']
    # Source
    source = xTree.Element('source')
    root.append(source)
    database = xTree.SubElement(source, 'database')
    database.text = 'unknown'
    # Size
    size = xTree.Element('size')
    root.append(size)
    width = xTree.SubElement(size, 'width')
    width.text = str(ann['size'][0])
    height = xTree.SubElement(size, 'height')
    height.text = str(ann['size'][1])
    depth = xTree.SubElement(size, 'depth')
    depth_selector = {'RGB':'3','L':'1'}        # To conform with imglable syntax
    the_depth = depth_selector[ann['depth']]
    depth.text = the_depth
    # Segmented
    segmented = xTree.SubElement(root,'segmented')
    segmented.text = '0'
    # Write all annotation boxes + classes
    for box in results['boxes']:
        the_object = xTree.Element("object")
        root.append(the_object)

        ob_name = xTree.SubElement(the_object, "name")
        ob_name.text = classes[str(box['class'])]

        pose = xTree.SubElement(the_object, "pose")
        pose.text = "Unspecified"
       
        trunc = xTree.SubElement(the_object, "truncated")
        trunc.text = '0'

        diff = xTree.SubElement(the_object, "difficult")
        diff.text = '0'

        bndbox = xTree.Element("bndbox")
        the_object.append(bndbox)

        xmin = xTree.SubElement(bndbox, "xmin")
        xmin.text = str(box['ROI'][0])
        
        ymin = xTree.SubElement(bndbox, "ymin")
        ymin.text = str(box['ROI'][1])

        xmax = xTree.SubElement(bndbox, "xmax")
        xmax.text = str(box['ROI'][2])

        ymax = xTree.SubElement(bndbox, "ymax")
        ymax.text = str(box['ROI'][3])

    tree = xTree.ElementTree(root)
    xmlstr = minidom.parseString(xTree.tostring(root)).toprettyxml(indent="   ")
    with open(voc_path, "wb") as fh:
        fh.write(xmlstr.encode('utf-8'))


if __name__ == '__main__':
    # Test
    ann = {"boxes": [{"conf": 0.9812983274459839, "class": 24, 
    "ROI": [488.7626953125, 758.47705078125, 631.1488647460938, 
    848.8037109375]}, {"conf": 0.9583034515380859, "class": 11, 
    "ROI": [335.9580383300781, 330.22967529296875, 500.98681640625, 
    582.5828857421875]}], 
    "path": "InImages/ANP_F2_2009_Aug_15_BL.JPG", 
    "size": [3233, 2157], "depth": "RGB", "name": "image1.jpg"}


