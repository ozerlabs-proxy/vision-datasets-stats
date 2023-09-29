"""
Holds functions needed to generate dataset statistics. 
There are two main functions that are used to generate the statistics:
    - generate_dataset_statistics
    - save_dataset_statistics

the functions will be implemented in the child classes of BaseDataset.
"""



import os
import json
import numpy as np
from typing import Dict, List, Tuple, Union
from collections import defaultdict
from pathlib import Path
from utils import utilities
from  utils.utilities import _isArrayLike

class BaseDataset:

    TAGS = [
            "created_by",
            "dataset_name",
            "description",
            "task",
            "images_count",
            "annotations_count",
            "_images_stats",
            "_categories_stats",
            "_super_categories_stats",
            "_boxes_stats",
            "_masks_stats"
        ]
    
    def __init__(self, 
                 extra_tags:list=None) -> None:

        self.dataset_statistics = defaultdict(dict)

        self.TAGS=BaseDataset.TAGS
        if not extra_tags is None:
            self.TAGS.extend(extra_tags)
        
        self.TAGS = list(set(self.TAGS))
        self.TAGS.sort()
        for tag in self.TAGS:
            self.dataset_statistics[tag] = None
    

    def generate_dataset_statistics(self) -> None:
        pass


    # save dataset statistics to a json file
    def save_dataset_statistics(self,
                                save_path:str="./summaries",
                                dataset_name:str=None,
                                file_name:str=None) -> None:
        """
        saves the dataset statistics summary to a json file with the name given name.
            Args:
                save_path: path to save the file
                file_name: name of the file to save

            Usage:
                >>> dataset.save_dataset_statistics(save_path='path/to/save', 
                                                        file_name='dataset_statistics.json')
        """
        
        save_path = Path(save_path)
        dataset_name = dataset_name if dataset_name else f"{self.__class__.__name__}"
        save_path = save_path / dataset_name

        save_path.mkdir(parents=True, exist_ok=True)
        file_name = file_name if file_name else f"{self.__class__.__name__}_stats.json"

        file_path = save_path / file_name
        assert file_path.suffix == '.json', 'file name must have .json extension'

        try:
            with open(file_path, 'w') as f:
                print(f'[INFO] saving ...: {file_name}')
                json.dump(self.dataset_statistics, f,default=utilities.np_encoder)
        except Exception as e:
            print(f'[ERROR] saving dataset statistics...: {e}')

        print(f'[INFO] dataset statistics saved to: {file_path}')

        

    ########## coco native functions ##########
    def info(self):
        """
        Print information about the annotation file.
        :return:
        """
        for key, value in self.dataset['info'].items():
            print('{}: {}'.format(key, value))

    def getAnnIds(self, imgIds=[], catIds=[], areaRng=[], iscrowd=None):
        """
        Get ann ids that satisfy given filter conditions. default skips that filter
        :param imgIds  (int array)     : get anns for given imgs
               catIds  (int array)     : get anns for given cats
               areaRng (float array)   : get anns for given area range (e.g. [0 inf])
               iscrowd (boolean)       : get anns for given crowd label (False or True)
        :return: ids (int array)       : integer array of ann ids
        """
        imgIds = imgIds if _isArrayLike(imgIds) else [imgIds]
        catIds = catIds if _isArrayLike(catIds) else [catIds]

        if len(imgIds) == len(catIds) == len(areaRng) == 0:
            anns = self.dataset['annotations']
        else:
            if not len(imgIds) == 0:
                lists = [self.imgToAnns[imgId] for imgId in imgIds if imgId in self.imgToAnns]
                anns = list(itertools.chain.from_iterable(lists))
            else:
                anns = self.dataset['annotations']
            anns = anns if len(catIds)  == 0 else [ann for ann in anns if ann['category_id'] in catIds]
            anns = anns if len(areaRng) == 0 else [ann for ann in anns if ann['area'] > areaRng[0] and ann['area'] < areaRng[1]]
        if not iscrowd == None:
            ids = [ann['id'] for ann in anns if ann['iscrowd'] == iscrowd]
        else:
            ids = [ann['id'] for ann in anns]
        return ids

    def getCatIds(self, catNms=[], supNms=[], catIds=[]):
        """
        filtering parameters. default skips that filter.
        :param catNms (str array)  : get cats for given cat names
        :param supNms (str array)  : get cats for given supercategory names
        :param catIds (int array)  : get cats for given cat ids
        :return: ids (int array)   : integer array of cat ids
        """
        catNms = catNms if _isArrayLike(catNms) else [catNms]
        supNms = supNms if _isArrayLike(supNms) else [supNms]
        catIds = catIds if _isArrayLike(catIds) else [catIds]

        if len(catNms) == len(supNms) == len(catIds) == 0:
            cats = self.dataset['categories']
        else:
            cats = self.dataset['categories']
            cats = cats if len(catNms) == 0 else [cat for cat in cats if cat['name']          in catNms]
            cats = cats if len(supNms) == 0 else [cat for cat in cats if cat['supercategory'] in supNms]
            cats = cats if len(catIds) == 0 else [cat for cat in cats if cat['id']            in catIds]
        ids = [cat['id'] for cat in cats]
        return ids

    def getImgIds(self, imgIds=[], catIds=[]):
        '''
        Get img ids that satisfy given filter conditions.
        :param imgIds (int array) : get imgs for given ids
        :param catIds (int array) : get imgs with all given cats
        :return: ids (int array)  : integer array of img ids
        '''
        imgIds = imgIds if _isArrayLike(imgIds) else [imgIds]
        catIds = catIds if _isArrayLike(catIds) else [catIds]

        if len(imgIds) == len(catIds) == 0:
            ids = self.imgs.keys()
        else:
            ids = set(imgIds)
            for i, catId in enumerate(catIds):
                if i == 0 and len(ids) == 0:
                    ids = set(self.catToImgs[catId])
                else:
                    ids &= set(self.catToImgs[catId])
        return list(ids)

    def loadAnns(self, ids=[]):
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying anns
        :return: anns (object array) : loaded ann objects
        """
        if _isArrayLike(ids):
            return [self.anns[id] for id in ids]
        elif type(ids) == int:
            return [self.anns[ids]]

    def loadCats(self, ids=[]):
        """
        Load cats with the specified ids.
        :param ids (int array)       : integer ids specifying cats
        :return: cats (object array) : loaded cat objects
        """
        if _isArrayLike(ids):
            return [self.cats[id] for id in ids]
        elif type(ids) == int:
            return [self.cats[ids]]

    def loadImgs(self, ids=[]):
        """
        Load anns with the specified ids.
        :param ids (int array)       : integer ids specifying img
        :return: imgs (object array) : loaded img objects
        """
        if _isArrayLike(ids):
            return [self.imgs[id] for id in ids]
        elif type(ids) == int:
            return [self.imgs[ids]]

    


        


