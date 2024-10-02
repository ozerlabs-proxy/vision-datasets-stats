# convert vedai to coco format
import sys
import os
sys.path.append(os.getcwd())

'''
scrip to convert vedai to coco format
script is ment to be run from the root directory of the project

python scripts/convert_vedai_to_coco_format.py

:: later on it will be possible to provide argument flags to the script
'''

from pathlib import Path
from utils import conversion_vedai_tools
from utils import utilities


# Path to the images and annotations
dataset_path = Path("data/vedai/")
annotations_dir ="annotations"
converted_annotations_dir = "converted_annotations"

#convert visdrone to coco format
# print("[INFO] Converting dataset to coco format...")
_coco_format = conversion_vedai_tools.convert_vedai_to_coco(dataset_path=dataset_path,
                            annotations_dir = annotations_dir)
# print("[INFO] done. ")
# save the json file
utilities.save_json(data=_coco_format, 
                        save_dir=str(dataset_path/converted_annotations_dir),
                        file_name="vedai_converted_to_coco_format.json")
 