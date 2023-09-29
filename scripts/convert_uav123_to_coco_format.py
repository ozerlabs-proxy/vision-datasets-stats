
import os
import sys
from pathlib import Path
sys.path.append(os.getcwd())
from utils import utilities
from utils import conversion_uav123_tools as conversion_tools

"""
    This script will convert dota format dataset to coco json format.
"""

_d_name="uav123"
# Path to the images and annotations
_d_path = Path(f"data/{_d_name}/")
annotations_dir ="annotations"
converted_annotations_dir = "converted_annotations"

#convert visdrone to coco format
# print("[INFO] Converting dataset to coco format...")
_coco_format = conversion_tools.convert_uav123_to_coco(DATA_PATH=_d_path,
                                                        annotations_dir = annotations_dir,
                                                        annotation_file = f"{_d_name}.json")
# print("[INFO] done. ")
# save the json file
utilities.save_json(data=_coco_format, 
                        save_dir=str(_d_path/converted_annotations_dir),
                        file_name=f"{_d_name}_converted_to_coco_format.json")
 