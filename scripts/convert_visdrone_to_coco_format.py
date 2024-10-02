# convert visdrone to coco format
import sys
import os
sys.path.append(os.getcwd())

'''
script is ment to be run from the root directory of the project
python scripts/convert_visdrone_to_coco_format.py
'''

from pathlib import Path
from utils import conversion_visdrone_tools
from utils import utilities


# Path to the images and annotations
visdrone_path = Path("data/visdrone/")
annotations_dir ="annotations"
converted_annotations_dir = "converted_annotations"

#convert visdrone to coco format
# print("[INFO] Converting dataset to coco format...")
visdrone_coco_format = conversion_visdrone_tools.convert_visdrone_to_coco(visdrone_path=visdrone_path,
                            annotations_dir = annotations_dir)
# print("[INFO] done. ")
# save the json file
utilities.save_json(data=visdrone_coco_format, 
                        save_dir=str(visdrone_path/converted_annotations_dir),
                        file_name="visdrone_converted_to_coco_format.json")
 