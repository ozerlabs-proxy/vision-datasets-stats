# convert kitti to coco format
import sys
import os
sys.path.append(os.getcwd())

'''
scrip to convert kitti to coco format
'''

from pathlib import Path
from utils import conversion_kitti_tools
from utils import utilities


# Path to the images and annotations
dataset_path = Path("data/kitti/")
annotations_dir ="label_2"
converted_annotations_dir = "converted_annotations"

#convert visdrone to coco format
print("[INFO] Converting dataset to coco format...")
_coco_format = conversion_kitti_tools.convert_kitti_to_coco(split="training",
                                                            DATA_PATH=dataset_path,
                                                            annotations_dir = annotations_dir)
print("[INFO] done. ")
# save the json file
utilities.save_json(data=_coco_format, 
                        save_dir=str(dataset_path/converted_annotations_dir),
                        file_name="kitti_converted_to_coco_format.json")
 