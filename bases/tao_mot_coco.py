import os
import json
from tqdm import tqdm
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

class TAO(BaseDatasetTracking):
    
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
        
        self.dataset_statistics['dataset_name'] = 'TAO'
        self.dataset_statistics['video_count'] = len(self.videos)
        self.dataset_statistics['description'] = 'TAO contains videos from 7 datasets: ArgoVerse, AVA, BDD-100k, Charades, HACS, LaSOT, and YFCC-100M.'
        self.dataset_statistics['created_by'] = 'TAO'
        self.dataset_statistics['task'] = 'MOT'
        self.dataset_statistics['info'] = self.dataset['info'] if 'info' in self.dataset else {}
        other_stats = coco_like_datasets_tracking.generate_stats_coco_like(self)
        self.dataset_statistics.update(other_stats)
        
        
    def createIndex(self):
        """Create index."""
        print('creating index...')
        anns, cats, imgs, vids , adjustedAnns= {}, {}, {}, {},{}
        imgToAnns, vidToInstances, instancesToImgs, catToVids,vidToCats, vidToImgs, vidToTracks,tracksToFrames, catsToTracks  = ( defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list), 
                                                                                    defaultdict(list)   
                                                                                    )
        
        print('indexing videos...')
        if 'videos' in self.dataset:
            for video in self.dataset['videos']:
                # video = copy.deepcopy(video)
                video.update({'file_names':[],'length':0})
                vids[video['id']] = video
        # image to video ids mapping
        imgToVid = {}
        if 'images' in self.dataset:
            for img in self.dataset['images']:
                imgToVid[img['id']] = img['video_id']
                
        # update annotations with video_id
        print('updating annotations with video_id...')
        if 'annotations' in self.dataset:
            annotations_with_video_id = []
            for ann in self.dataset['annotations']:
                ann.update({'video_id': imgToVid[ann['image_id']]})
                annotations_with_video_id.append(ann)
            self.dataset['annotations'] = annotations_with_video_id
            
        print('indexing annotations...')
        if 'annotations' in self.dataset:
            for ann in tqdm(self.dataset['annotations']):
                
                anns[ann['id']] = ann
                if(ann["track_id"] not in adjustedAnns):
                    adjustedAnns[ann["track_id"]] = {
                                                        "id": ann["track_id"],
                                                        "video_id": ann["video_id"],
                                                        "category_id": ann["category_id"],
                                                        "areas":[],
                                                        "bboxes":[],
                                                        "segmentations":[],
                                                        "iscrowd": 0
                                                        }
                
                adjustedAnns[ann["track_id"]]["areas"].append(ann["area"])
                adjustedAnns[ann["track_id"]]["bboxes"].append(ann["bbox"])
                if "segmentation" in ann:
                    adjustedAnns[ann["track_id"]]["segmentations"].append(ann["segmentation"])
                if 'id' in ann:
                    vidToTracks[ann['video_id']].append(ann['track_id'])
            vidToTracks = {k:list(set(v)) for k,v in vidToTracks.items()}
                        
        print('frames indexing...')
        if 'images' in self.dataset:
            for img in self.dataset['images']:
                vidToImgs[img['video_id']].append(img)
                assert "file_names" in vids[img['video_id']].keys(), "file_names not in vids"
                vids[img['video_id']]['file_names'].append(img['file_name'])
                imgs[img['id']] = img
                
            #update video file_names and length
            for vid in vids.values():
                vid['file_names'] = list(set((vid['file_names'])))
                vid['length'] = len(vid['file_names'])
                
                
        print('indexing categories...')
        if 'categories' in self.dataset:
            for cat in self.dataset['categories']:
                cats[cat['id']] = cat
        
        print('indexing categories to videos...')
        if 'annotations' in self.dataset and 'categories' in self.dataset:
            for ann in tqdm(self.dataset['annotations']):
                catToVids[ann['category_id']].append(ann['video_id'])
                vidToCats[ann['video_id']].append(ann['category_id'])
                catsToTracks[ann['category_id']].append(ann['track_id'])
            
            catToVids = {k:list(set(v)) for k,v in catToVids.items()}
            vidToCats = {k:list(set(v)) for k,v in vidToCats.items()}
            catsToTracks = {k:list(set(v)) for k,v in catsToTracks.items()}
            
                    
        print('indexing images to annotations...')   
        if 'annotations' in tqdm(self.dataset):
            for ann in self.dataset['annotations']:
                imgToAnns[ann['image_id']].append(ann)
                anns[ann['id']] = ann
                if 'id' in ann:
                    instancesToImgs[ann['id']].append(ann['image_id'])
                    # if 'video_id' in ann and  ann['instance_id'] not in vidToInstances[ann['video_id']]:
                    vidToInstances[ann['id']].append(ann['id'])
            instancesToImgs = {k:list(set(v)) for k,v in instancesToImgs.items()}
            vidToInstances = {k:list(set(v)) for k,v in vidToInstances.items()}
                        
        
        # adjustedAnns = list(adjustedAnns.values())
        if 'annotations' in self.dataset:
            for ann in tqdm(adjustedAnns.values()):
                areas_or_boxes_or_segmentations = ann['areas'] if 'areas' in ann \
                    else ann['bboxes'] if 'bboxes' in ann \
                    else ann['segmentations'] if 'segmentations' in ann \
                    else None
                    
                non_none_boxes_filenames = []
                if areas_or_boxes_or_segmentations is not None:
                    
                    #get non none boxes indices
                    non_none_boxes = [i for i, e in enumerate(areas_or_boxes_or_segmentations) if e is not None]
                    #get filenames of non none boxes
                        
                    try:
                        non_none_boxes_filenames = np.array(vids[ann['video_id']]["file_names"])[non_none_boxes]
                    except:
                        non_none_boxes_filenames = np.array(vids[ann['video_id']]["file_names"])
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
        self.adjustedAnns = adjustedAnns
        self.vidToInstances = vidToInstances
        self.instancesToImgs = instancesToImgs
