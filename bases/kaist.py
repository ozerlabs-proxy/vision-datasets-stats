__author__ = 'nalain'
__version__ = 'v1.0'


import json
import time
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import numpy as np
import copy
import itertools
# from . import mask as maskUtils
import os
from collections import defaultdict
import sys
PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 2:
    from urllib import urlretrieve
elif PYTHON_VERSION == 3:
    from urllib.request import urlretrieve

# has methods to be implemented
from .base_dataset_functionality import BaseDataset
from   utils import coco_like_datasets  
from  utils.utilities import _isArrayLike

class KAIST(BaseDataset):
    def __init__(self, annotation_file=None):
        """
        same as skydata and coco 
        """
        super().__init__(extra_tags=['task'])

        # load dataset
        self.dataset,self.anns,self.cats,self.imgs = dict(),dict(),dict(),dict()
        self.imgToAnns, self.catToImgs = defaultdict(list), defaultdict(list)
        if not annotation_file == None:
            print('loading annotations into memory...')
            tic = time.time()
            dataset = json.load(open(annotation_file, 'r'))
            assert type(dataset)==dict, 'annotation file format {} not supported'.format(type(dataset))
            print('Done (t={:0.2f}s)'.format(time.time()- tic))
            self.dataset = dataset
            self.createIndex()

    def generate_dataset_statistics(self):
        """
            This function generates the dataset statistics. including: counts.
            The statistics are saved in a dictionary with keys as the tags and values as the statistics.
        """                                                                                             
        print(f"[INFO] Generating dataset statistics for the {self.__class__.__name__}...")
        
        self.dataset_statistics['dataset_name'] = "KAIST_roboflow"                                                                                                                                                                                                                   
        self.dataset_statistics['dataset_size'] = len(self.dataset['images'])
        self.dataset_statistics['description'] = 'KAIST  dataset'
        self.dataset_statistics['created_by'] = 'KAIST'
        self.dataset_statistics['task'] = 'detection'
        self.dataset_statistics['info'] = self.dataset['info']
        other_stats = coco_like_datasets.generate_stats_coco_like(self)
        self.dataset_statistics.update(other_stats)

        print(f"[INFO] Dataset statistics generated for the {self.__class__.__name__}.")
    

    def createIndex(self):
        # create index
        print('creating index...')
        anns, cats, imgs = {}, {}, {}
        imgToAnns,catToImgs = defaultdict(list),defaultdict(list)
        if 'annotations' in self.dataset:
            for ann in self.dataset['annotations']:
                imgToAnns[ann['image_id']].append(ann)
                anns[ann['id']] = ann

        if 'images' in self.dataset:
            for img in self.dataset['images']:
                imgs[img['id']] = img

        if 'categories' in self.dataset:
            for cat in self.dataset['categories']:
                cats[cat['id']] = cat

        if 'annotations' in self.dataset and 'categories' in self.dataset:
            for ann in self.dataset['annotations']:
                catToImgs[ann['category_id']].append(ann['image_id'])

        print('index created!')

        # create class members
        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToImgs = catToImgs
        self.imgs = imgs
        self.cats = cats

