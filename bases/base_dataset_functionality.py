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

        


    


        


