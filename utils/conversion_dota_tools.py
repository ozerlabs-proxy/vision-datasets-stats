import sys
import codecs
import numpy as np
import shapely.geometry as shgeo
import os
import re
import math
import cv2
import json
from PIL import Image
from pathlib import Path
from  tqdm import tqdm

# import polyiou
"""
    some basic functions which are useful for process DOTA data
"""

wordname_15 = ['plane', 
                    'baseball-diamond', 
                    'bridge', 
                    'ground-track-field', 
                    'small-vehicle', 
                    'large-vehicle', 
                    'ship', 
                    'tennis-court',
                    'basketball-court', 
                    'storage-tank',  
                    'soccer-ball-field', 
                    'roundabout', 
                    'harbor', 
                    'swimming-pool', 
                    'helicopter']

wordname_16 = ['plane', 
                    'baseball-diamond', 
                    'bridge', 
                    'ground-track-field', 
                    'small-vehicle', 
                    'large-vehicle', 
                    'ship', 
                    'tennis-court',
                    'basketball-court', 
                    'storage-tank',  
                    'soccer-ball-field', 
                    'roundabout', 
                    'harbor', 
                    'swimming-pool', 
                    'helicopter', 
                    'container-crane']

wordname_v2 = ['plane', 
                    'baseball-diamond', 
                    'bridge', 
                    'ground-track-field', 
                    'small-vehicle', 
                    'large-vehicle', 
                    'ship', 
                    'tennis-court',
                    'basketball-court',
                    'storage-tank',  
                    'soccer-ball-field', 
                    'roundabout', 
                    'harbor', 
                    'swimming-pool', 
                    'helicopter', 
                    'container-crane',
                    'airport', 
                    'helipad',]

def custombasename(fullname):
    return os.path.basename(os.path.splitext(fullname)[0])

def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles

def TuplePoly2Poly(poly):
    outpoly = [poly[0][0], poly[0][1],
                       poly[1][0], poly[1][1],
                       poly[2][0], poly[2][1],
                       poly[3][0], poly[3][1]
                       ]
    return outpoly

def parse_dota_poly_refactor(filename, code):
    """
        parse the dota ground truth in the format:
        [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    """
    objects = []
    #print('filename:', filename)
    f = []
    if (sys.version_info >= (3, 5)):
        fd = open(filename, 'r')
        f = fd
    elif (sys.version_info >= 2.7):
        fd = codecs.open(filename, 'r', code)
        f = fd
    # count = 0
    while True:
        line = f.readline()
        # count = count + 1
        # if count < 2:
        #     continue
        if line:
            splitlines = line.strip().split(' ')
            object_struct = {}
            ### clear the wrong name after check all the data
            #if (len(splitlines) >= 9) and (splitlines[8] in classname):
            if (len(splitlines) < 9):
                continue
            if (len(splitlines) >= 9):
                    object_struct['name'] = splitlines[8]
            if (len(splitlines) == 9):
                object_struct['difficult'] = '0'
            elif (len(splitlines) >= 10):
                # if splitlines[9] == '1':
                # if (splitlines[9] == 'tr'):
                #     object_struct['difficult'] = '1'
                # else:
                object_struct['difficult'] = splitlines[9]
                # else:
                #     object_struct['difficult'] = 0
            object_struct['poly'] = [(float(splitlines[0]), float(splitlines[1])),
                                     (float(splitlines[2]), float(splitlines[3])),
                                     (float(splitlines[4]), float(splitlines[5])),
                                     (float(splitlines[6]), float(splitlines[7]))
                                     ]
            gtpoly = shgeo.Polygon(object_struct['poly'])
            object_struct['area'] = gtpoly.area
            # poly = list(map(lambda x:np.array(x), object_struct['poly']))
            # object_struct['long-axis'] = max(distance(poly[0], poly[1]), distance(poly[1], poly[2]))
            # object_struct['short-axis'] = min(distance(poly[0], poly[1]), distance(poly[1], poly[2]))
            # if (object_struct['long-axis'] < 15):
            #     object_struct['difficult'] = '1'
            #     global small_count
            #     small_count = small_count + 1
            objects.append(object_struct)
        else:
            break
    return objects

def parse_dota_poly(filename):
    """
        parse the dota ground truth in the format:
        [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    """
    objects = []
    # print('filename:', filename)
    f = []
    if (sys.version_info >= (3, 5)):
        fd = open(filename, 'r')
        f = fd
    elif (sys.version_info >= 2.7):
        fd = codecs.open(filename, 'r')
        f = fd
    # count = 0
    while True:
        line = f.readline()
        # count = count + 1
        # if count < 2:
        #     continue
        if line:
            splitlines = line.strip().split(' ')
            object_struct = {}
            ### clear the wrong name after check all the data
            #if (len(splitlines) >= 9) and (splitlines[8] in classname):
            if (len(splitlines) < 9):
                continue
            if (len(splitlines) >= 9):
                    object_struct['name'] = splitlines[8]
            if (len(splitlines) == 9):
                object_struct['difficult'] = '0'
            elif (len(splitlines) >= 10):
                # if splitlines[9] == '1':
                # if (splitlines[9] == 'tr'):
                #     object_struct['difficult'] = '1'
                # else:
                object_struct['difficult'] = splitlines[9]
                # else:
                #     object_struct['difficult'] = 0
            object_struct['poly'] = [(float(splitlines[0]), float(splitlines[1])),
                                     (float(splitlines[2]), float(splitlines[3])),
                                     (float(splitlines[4]), float(splitlines[5])),
                                     (float(splitlines[6]), float(splitlines[7]))
                                     ]
            gtpoly = shgeo.Polygon(object_struct['poly'])
            object_struct['area'] = gtpoly.area
            # poly = list(map(lambda x:np.array(x), object_struct['poly']))
            # object_struct['long-axis'] = max(distance(poly[0], poly[1]), distance(poly[1], poly[2]))
            # object_struct['short-axis'] = min(distance(poly[0], poly[1]), distance(poly[1], poly[2]))
            # if (object_struct['long-axis'] < 15):
            #     object_struct['difficult'] = '1'
            #     global small_count
            #     small_count = small_count + 1
            objects.append(object_struct)
        else:
            break
    return objects

def parse_dota_poly2(filename):
    """
        parse the dota ground truth in the format:
        [x1, y1, x2, y2, x3, y3, x4, y4]
    """
    objects = parse_dota_poly(filename)
    for obj in objects:
        obj['poly'] = TuplePoly2Poly(obj['poly'])
        obj['poly'] = list(map(int, obj['poly']))
    return objects

def parse_dota_rec(filename):
    """
        parse the dota ground truth in the bounding box format:
        "xmin, ymin, xmax, ymax"
    """
    objects = parse_dota_poly(filename)
    for obj in objects:
        poly = obj['poly']
        bbox = dots4ToRec4(poly)
        obj['bndbox'] = bbox
    return objects
## bounding box transfer for varies format

def dots4ToRec4(poly):
    xmin, xmax, ymin, ymax = min(poly[0][0], min(poly[1][0], min(poly[2][0], poly[3][0]))), \
                            max(poly[0][0], max(poly[1][0], max(poly[2][0], poly[3][0]))), \
                             min(poly[0][1], min(poly[1][1], min(poly[2][1], poly[3][1]))), \
                             max(poly[0][1], max(poly[1][1], max(poly[2][1], poly[3][1])))
    return xmin, ymin, xmax, ymax
def dots4ToRec8(poly):
    xmin, ymin, xmax, ymax = dots4ToRec4(poly)
    return xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax
    #return dots2ToRec8(dots4ToRec4(poly))
def dots2ToRec8(rec):
    xmin, ymin, xmax, ymax = rec[0], rec[1], rec[2], rec[3]
    return xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax

def groundtruth2Task1(srcpath, dstpath):
    filelist = GetFileFromThisRootDir(srcpath)
    # names = [custombasename(x.strip())for x in filelist]
    filedict = {}
    for cls in wordname_15:
        fd = open(os.path.join(dstpath, 'Task1_') + cls + r'.txt', 'w')
        filedict[cls] = fd
    for filepath in filelist:
        objects = parse_dota_poly2(filepath)

        subname = custombasename(filepath)
        pattern2 = re.compile(r'__([\d+\.]+)__\d+___')
        rate = re.findall(pattern2, subname)[0]

        for obj in objects:
            category = obj['name']
            difficult = obj['difficult']
            poly = obj['poly']
            if difficult == '2':
                continue
            if rate == '0.5':
                outline = custombasename(filepath) + ' ' + '1' + ' ' + ' '.join(map(str, poly))
            elif rate == '1':
                outline = custombasename(filepath) + ' ' + '0.8' + ' ' + ' '.join(map(str, poly))
            elif rate == '2':
                outline = custombasename(filepath) + ' ' + '0.6' + ' ' + ' '.join(map(str, poly))

            filedict[category].write(outline + '\n')

def Task2groundtruth_poly(srcpath, dstpath):
    thresh = 0.1
    filedict = {}
    Tasklist = GetFileFromThisRootDir(srcpath, '.txt')

    for Taskfile in Tasklist:
        idname = custombasename(Taskfile).split('_')[-1]
        # idname = datamap_inverse[idname]
        f = open(Taskfile, 'r')
        lines = f.readlines()
        for line in lines:
            if len(line) == 0:
                continue
            # print('line:', line)
            splitline = line.strip().split(' ')
            filename = splitline[0]
            confidence = splitline[1]
            bbox = splitline[2:]
            if float(confidence) > thresh:
                if filename not in filedict:
                    # filedict[filename] = codecs.open(os.path.join(dstpath, filename + '.txt'), 'w', 'utf_16')
                    filedict[filename] = codecs.open(os.path.join(dstpath, filename + '.txt'), 'w')
                # poly = dots2ToRec8(bbox)
                poly = bbox
                #               filedict[filename].write(' '.join(poly) + ' ' + idname + '_' + str(round(float(confidence), 2)) + '\n')
            # print('idname:', idname)

            # filedict[filename].write(' '.join(poly) + ' ' + idname + '_' + str(round(float(confidence), 2)) + '\n')

                filedict[filename].write(' '.join(poly) + ' ' + idname + '\n')


def polygonToRotRectangle(bbox):
    """
    :param bbox: The polygon stored in format [x1, y1, x2, y2, x3, y3, x4, y4]
    :return: Rotated Rectangle in format [cx, cy, w, h, theta]
    """
    bbox = np.array(bbox,dtype=np.float32)
    bbox = np.reshape(bbox,newshape=(2,4),order='F')
    angle = math.atan2(-(bbox[0,1]-bbox[0,0]),bbox[1,1]-bbox[1,0])

    center = [[0],[0]]

    for i in range(4):
        center[0] += bbox[0,i]
        center[1] += bbox[1,i]

    center = np.array(center,dtype=np.float32)/4.0

    R = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]], dtype=np.float32)

    normalized = np.matmul(R.transpose(),bbox-center)

    xmin = np.min(normalized[0,:])
    xmax = np.max(normalized[0,:])
    ymin = np.min(normalized[1,:])
    ymax = np.max(normalized[1,:])

    w = xmax - xmin + 1
    h = ymax - ymin + 1

    return [float(center[0]),float(center[1]),w,h,angle]

def cal_line_length(point1, point2):
    return math.sqrt( math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

def get_best_begin_point(coordinate):
    x1 = coordinate[0][0]
    y1 = coordinate[0][1]
    x2 = coordinate[1][0]
    y2 = coordinate[1][1]
    x3 = coordinate[2][0]
    y3 = coordinate[2][1]
    x4 = coordinate[3][0]
    y4 = coordinate[3][1]
    xmin = min(x1, x2, x3, x4)
    ymin = min(y1, y2, y3, y4)
    xmax = max(x1, x2, x3, x4)
    ymax = max(y1, y2, y3, y4)
    combinate = [[[x1, y1], [x2, y2], [x3, y3], [x4, y4]], [[x2, y2], [x3, y3], [x4, y4], [x1, y1]],
                 [[x3, y3], [x4, y4], [x1, y1], [x2, y2]], [[x4, y4], [x1, y1], [x2, y2], [x3, y3]]]
    dst_coordinate = [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]]
    force = 100000000.0
    force_flag = 0
    for i in range(4):
        temp_force = cal_line_length(combinate[i][0], dst_coordinate[0]) + cal_line_length(combinate[i][1],
                                                                                           dst_coordinate[
                                                                                               1]) + cal_line_length(
            combinate[i][2], dst_coordinate[2]) + cal_line_length(combinate[i][3], dst_coordinate[3])
        if temp_force < force:
            force = temp_force
            force_flag = i
    if force_flag != 0:
        print("choose one direction!")
    return  combinate[force_flag]

def convert_dota_to_coco(srcpath : str,  
                   annotations_dir : str = None,
                   cls_names : list = wordname_v2, 
                   difficult ='2'):
    
    """
        COnvert dota format to coco json format. 

        Args:
            srcpath (str): path to the dota dataset
            annotations_dir (str): path to the annotations directory
            cls_names (list): list of class names
            difficult (str): difficult level
        Returns:
            None
        Info:
            # set difficult to filter '2', '1', or do not filter, set '-1'
        Usage:
            >>> DOTA2COCOTrain(srcpath,
                                annotations_dir, 
                                cls_names, 
                                difficult)
    """
    

    imageparent = os.path.join(srcpath, 'images')
    dota_txt_annotations = Path(srcpath) if not annotations_dir else Path(srcpath) / annotations_dir
    labelparent = os.path.join(str(dota_txt_annotations), 'labelTxt')

    data_dict = {
        "info": {
            "description": "DOTA  Dataset",
            "url": "https://captain-whu.github.io/DOTA/dataset.html",
            "version": "v2.0",
            "year": 2019,
            "contributor": "DOTA Team",
            "date_created": "2019"},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    for idex, name in enumerate(cls_names):
        single_cat = {'id': idex + 1, 'name': name, 'supercategory': name}
        data_dict['categories'].append(single_cat)

    inst_count = 1
    image_id = 1
    
    filenames = GetFileFromThisRootDir(labelparent)

    print("[INFO] converting format...")
    for file in tqdm(filenames):

        basename = custombasename(file)
        # image_id = int(basename[1:])

        imagepath = os.path.join(imageparent, basename + '.png')
            
        try:
            img = cv2.imread(imagepath)  
        except:
            print("Error: ", imagepath)
            continue

        height, width, c = img.shape
        single_image = {}
        single_image['file_name'] = basename + '.png'
        single_image['id'] = image_id
        single_image['width'] = width
        single_image['height'] = height
        data_dict['images'].append(single_image)

        # annotations
        objects = parse_dota_poly2(file)
        for obj in objects:
            if obj['difficult'] == difficult:
                print('difficult: ', difficult)
                continue
            single_obj = {}
            single_obj['area'] = obj['area']
            single_obj['category_id'] = cls_names.index(obj['name']) + 1
            single_obj['segmentation'] = []
            single_obj['segmentation'].append(obj['poly'])
            single_obj['iscrowd'] = 0
            xmin, ymin, xmax, ymax = min(obj['poly'][0::2]), min(obj['poly'][1::2]), \
                                        max(obj['poly'][0::2]), max(obj['poly'][1::2])

            width, height = xmax - xmin, ymax - ymin
            
            single_obj['bbox'] = xmin, ymin, width, height
            single_obj['image_id'] = image_id
            data_dict['annotations'].append(single_obj)
            single_obj['id'] = inst_count
            inst_count = inst_count + 1
        image_id = image_id + 1
    
    return data_dict

def convert_dota_to_coco_test(srcpath, 
                              destfile, 
                              cls_names):
    
    """
        COnvert dota format to coco json format.
        #TODO incomplete (not updated)
    """
    imageparent = os.path.join(srcpath, 'images')
    data_dict = {}

    data_dict['images'] = []
    data_dict['categories'] = []
    for idex, name in enumerate(cls_names):
        single_cat = {'id': idex + 1, 'name': name, 'supercategory': name}
        data_dict['categories'].append(single_cat)

    image_id = 1
    with open(destfile, 'w') as f_out:
        filenames = GetFileFromThisRootDir(imageparent)
        for file in filenames:
            basename = custombasename(file)
            imagepath = os.path.join(imageparent, basename + '.png')
            img = Image.open(imagepath)
            height = img.height
            width = img.width

            single_image = {}
            single_image['file_name'] = basename + '.png'
            single_image['id'] = image_id
            single_image['width'] = width
            single_image['height'] = height
            data_dict['images'].append(single_image)

            image_id = image_id + 1
        json.dump(data_dict, f_out)
