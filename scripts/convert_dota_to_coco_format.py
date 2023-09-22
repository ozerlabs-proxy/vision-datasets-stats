
import os
import sys
from pathlib import Path
sys.path.append(os.getcwd())
from utils import utilities
from utils import conversion_dota_tools

"""
    This script will convert dota format dataset to coco json format.
"""


wordname_v2 = ['plane', 
                    'baseball-diamond', 
                    'bridge', 
                    'ground-track-field', 
                    'small-vehicle', 
                    'large-vehicle', 
                    'ship', 
                    'tennis-court',
                    'basketball-court',
                    'storage-tank',  
                    'soccer-ball-field', 
                    'roundabout', 
                    'harbor', 
                    'swimming-pool', 
                    'helicopter', 
                    'container-crane',
                    'airport', 
                    'helipad',]


# Path to the images and annotations
dota_path = Path('data/dota')
_outputdir = dota_path / 'converted_annotations'
_outputdir.mkdir(parents=True, exist_ok=True)



print(f"[INFO] Converting DOTA to COCO format...")
parsed_annotations=conversion_dota_tools.convert_dota_to_coco(srcpath=str(dota_path),
                                            annotations_dir='labelTxt-v2.0',
                                            cls_names=wordname_v2)
print(f"[INFO] Converting DOTA to COCO format completed.")

# save the json file
utilities.save_json(data=parsed_annotations, 
                save_dir=str(_outputdir),
                file_name='dotav2_converted_to_coco.json')  

