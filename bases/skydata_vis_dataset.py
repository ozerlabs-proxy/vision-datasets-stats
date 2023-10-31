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
from tqdm import tqdm

# has methods to be implemented
from .base_dataset_functionality import BaseDatasetTracking
from   utils import coco_like_datasets_tracking 
from  utils.utilities import _isArrayLike

class SkyDataVis(BaseDatasetTracking):
    
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
        
        self.dataset_statistics['dataset_name'] = 'SkyData'
        self.dataset_statistics['video_count'] = len(self.videos)
        self.dataset_statistics['description'] = 'SkyDataVis Video Instance Segmentation dataset'
        self.dataset_statistics['created_by'] = 'Ozerlabs'
        self.dataset_statistics['task'] = 'Vis'
        self.dataset_statistics['info'] = self.dataset['info'] if 'info' in self.dataset else {}
        other_stats = coco_like_datasets_tracking.generate_stats_coco_like(self)
        self.dataset_statistics.update(other_stats)
        
        
    def createIndex(self):
        """Create index."""
        print('creating index...')
        anns, cats, imgs, vids = {}, {}, {}, {}
        imgToAnns, catToVids,vidToCats, vidToImgs, vidToTracks,tracksToFrames, catsToTracks  = ( defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list)
                                                                                    )
        if 'videos' in self.dataset:
            for video in self.dataset['videos']:
                vids[video['id']] = video

        if 'annotations' in self.dataset:
            print('building index by Tracks...')
            for ann in tqdm(self.dataset['annotations']):
                anns[ann['id']] = ann
                if 'id' in ann:
                    if 'video_id' in ann and ann['id'] not in vidToTracks[ann['video_id']]:
                        vidToTracks[ann['video_id']].append(ann['id'])

        if 'images' in self.dataset:
            for img in self.dataset['images']:
                vidToImgs[img['video_id']].append(img)
                imgs[img['id']] = img

        if 'categories' in self.dataset:
            for cat in self.dataset['categories']:
                cats[cat['id']] = cat

        if 'annotations' in self.dataset and 'categories' in self.dataset:
            print('building index by category ids...')
            for ann in tqdm(self.dataset['annotations']):
                if ann["video_id"] not in catToVids[ann['category_id']]:
                    catToVids[ann['category_id']].append(ann['video_id'])
                if ann["category_id"] not in vidToCats[ann['video_id']]:
                    vidToCats[ann['video_id']].append(ann['category_id'])
                if ann["id"] not in catsToTracks[ann['category_id']]:
                    catsToTracks[ann['category_id']].append(ann['id'])
        
        if 'annotations' in self.dataset:
            print('building index by areas...')
            for ann in tqdm(self.dataset['annotations']):
                areas_or_boxes_or_segmentations = ann['areas'] if 'areas' in ann \
                    else ann['segmentations'] if 'segmentations' in ann \
                    else ann['boxes'] if 'boxes' in ann \
                    else None
                    
                non_none_boxes_filenames = []
                if areas_or_boxes_or_segmentations is not None:
                    
                    #get non none boxes indices
                    non_none_boxes = [i for i, e in enumerate(areas_or_boxes_or_segmentations) if e is not None]
                    #get filenames of non none boxes
                    
                    non_none_boxes_filenames = np.array(vids[ann['video_id']]["file_names"])[non_none_boxes]
                
                tracksToFrames[ann['id']] = non_none_boxes_filenames
        

        print('index created!')

        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToVids = catToVids
        self.imgs = imgs
        self.cats = cats
        self.videos = vids
        self.vidToImgs = vidToImgs
        self.vidToTracks = vidToTracks
        self.catsToTracks = catsToTracks
        self.vidToCats = vidToCats
        self.tracksToFrames = tracksToFrames
