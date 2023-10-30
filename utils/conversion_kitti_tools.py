"""
convert kitti dataset for detection to coco format

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, glob
from scipy.io import loadmat
from collections import defaultdict
import numpy as np
import json
import PIL.Image as Image
import os 
from pathlib import Path
from tqdm import tqdm
import json
import numpy as np

import glob

import os

'''
#Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.
'''

# GLOBAL constants
cats = ['Pedestrian', 'Car', 'Cyclist', 'Van', 'Truck',  'Person_sitting',
        'Tram', 'Misc', 'DontCare']
cat_ids = {cat: i + 1 for i, cat in enumerate(cats)}
# cat_info = [{"name": "pedestrian", "id": 1}, {"name": "vehicle", "id": 2}]
F = 721
H = 384 # 375
W = 1248 # 1242
EXT = [45.75, -0.34, 0.005]
CALIB = np.array([[F, 0, W / 2, EXT[0]], [0, F, H / 2, EXT[1]], 
                  [0, 0, 1, EXT[2]]], dtype=np.float32)




# bounding box format: [x1, y1, w, h]
def _bbox_to_coco_bbox(bbox):
  return [(bbox[0]), (bbox[1]),
          (bbox[2] - bbox[0]), (bbox[3] - bbox[1])]


def convert_kitti_to_coco(split : str ="training",
                          DATA_PATH : str = 'data/kitti/',
                          annotations_dir : str = 'label_2'):
  
  """
  convert the kitti dataset to coco format
  """
  cat_info = []
  for i, cat in enumerate(cats):
    cat_info.append({'name': cat, 'id': i + 1})


  image_set_path = Path(DATA_PATH)/str(split)
  ann_dir = Path(DATA_PATH)/ str(split)/ annotations_dir

  ret = {
        "info": {
            "description": "KITTI  Dataset",
            "url": "https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark",
            "version": "vDet",
            "year": 2012,
            "contributor": "A. Geiger and the Team",
            "date_created": " 2012"},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": cat_info
    }
 
  annotation_files = list(ann_dir.glob('*.txt'))
  seen_image_ids = []

  for ann_file in tqdm(annotation_files):

      file_name = Path(ann_file).stem
      image_id= int(file_name)

      # load the image fro dimensions
      img_file = image_set_path / 'image_2' / '{}.png'.format(file_name)
      try:
        img = Image.open(img_file)
        W, H = img.size
      except:
        print("error loading image: ", img_file)
        W, H = 1, 1
        
      image_info = {'file_name': '{}.png'.format(file_name),
                    'id': image_id,
                    'calib':'',
                    'width': W,
                    'height': H
                    }
      if image_info['id'] not in seen_image_ids:
        ret['images'].append(image_info)
        seen_image_ids.append(image_info['id'])
     

      anns = open(ann_file, 'r')
      
      for ann_ind, txt in enumerate(anns):
        tmp = txt[:-1].split(' ')
        cat_id = cat_ids[tmp[0]]
        truncated = int(float(tmp[1]))
        occluded = int(tmp[2])
        alpha = float(tmp[3])
        bbox = [float(tmp[4]), float(tmp[5]), float(tmp[6]), float(tmp[7])]
        dim = [float(tmp[8]), float(tmp[9]), float(tmp[10])]
        location = [float(tmp[11]), float(tmp[12]), float(tmp[13])]
        rotation_y = float(tmp[14])
        bbox=_bbox_to_coco_bbox(bbox)
        ann = {'image_id': image_id,
                'id': int(len(ret['annotations']) + 1),
                'category_id': cat_id,
                'dim': dim,
                'bbox': bbox,
                'depth': location[2],
                'alpha': alpha,
                'truncated': truncated,
                'occluded': occluded,
                'location': location,
                'rotation_y': rotation_y,
                'iscrowd': 0,
                'segmentation': [],
                'area': float(bbox[2]) * float(bbox[3])
                }
        ret['annotations'].append(ann)
     

  print("# images: ", len(ret['images']))
  print("# annotations: ", len(ret['annotations']))

  return ret


