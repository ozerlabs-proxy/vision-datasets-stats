import os
import json
import numpy as np
from typing import Dict, List, Tuple, Union
from collections import defaultdict
from pathlib import Path
from utils import utilities
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

# has methods to be implemented
from .base_dataset_functionality import BaseDatasetTracking
from   utils import coco_like_datasets_tracking 
from  utils.utilities import _isArrayLike

class YoutubeVisDataset(BaseDatasetTracking):
    
    def __init__(self, annotation_file=None):
        """
        """
        super().__init__(extra_tags=['task'])

        # load dataset
        self.dataset, self.anns, self.cats,self.imgs ,self.videos = dict(),dict(),dict(),dict(), dict()
        self.imgToAnns, self.catToImgs , self.instancesToImgs , self.vidToInstances , self.vidToImgs = ( defaultdict(list), 
                                                                                                            defaultdict(list),
                                                                                                            defaultdict(list),
                                                                                                            defaultdict(list),
                                                                                                            defaultdict(list)
                                                                                                            )
            
        
        if not annotation_file == None:
            print('[INFO] loading annotations into memory...')
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
            
            self.dataset_statistics['dataset_name'] = 'COCO'
            self.dataset_statistics['dataset_size'] = len(self.dataset['images'])
            self.dataset_statistics['description'] = 'COCO dataset'
            self.dataset_statistics['created_by'] = 'Microsoft'
            self.dataset_statistics['task'] = 'detection'
            self.dataset_statistics['info'] = self.dataset['info']
            other_stats = coco_like_datasets_tracking.generate_stats_coco_like(self)
            self.dataset_statistics.update(other_stats)
        
        
    def createIndex(self):
        """Create index."""
        print('creating index...')
        anns, cats, imgs, vids = {}, {}, {}, {}
        imgToAnns, catToImgs, vidToImgs, vidToInstances,instancesToImgs = ( defaultdict(list), 
                                                                            defaultdict(list), 
                                                                            defaultdict(list), 
                                                                            defaultdict(list), 
                                                                            defaultdict(list)
                                                                            )
        if 'videos' in self.dataset:
            for video in self.dataset['videos']:
                vids[video['id']] = video

        if 'annotations' in self.dataset:
            for ann in self.dataset['annotations']:
                imgToAnns[ann['image_id']].append(ann)
                anns[ann['id']] = ann
                if 'instance_id' in ann:
                    instancesToImgs[ann['instance_id']].append(ann['image_id'])
                    if 'video_id' in ann and \
                        ann['instance_id'] not in \
                            vidToInstances[ann['video_id']]:
                        vidToInstances[ann['video_id']].append(
                            ann['instance_id'])

        if 'images' in self.dataset:
            for img in self.dataset['images']:
                vidToImgs[img['video_id']].append(img)
                imgs[img['id']] = img

        if 'categories' in self.dataset:
            for cat in self.dataset['categories']:
                cats[cat['id']] = cat

        if 'annotations' in self.dataset and 'categories' in self.dataset:
            for ann in self.dataset['annotations']:
                catToImgs[ann['category_id']].append(ann['image_id'])

        print('index created!')

        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToImgs = catToImgs
        self.imgs = imgs
        self.cats = cats
        self.videos = vids
        self.vidToImgs = vidToImgs
        self.vidToInstances = vidToInstances
        self.instancesToImgs = instancesToImgs