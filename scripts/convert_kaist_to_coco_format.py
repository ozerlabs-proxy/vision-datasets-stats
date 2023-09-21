# convert kaist to coco format
import sys
import os
sys.path.append(os.getcwd())

'''
script is ment to be run from the root directory of the project
python ./scripts/convert_kaist_to_coco_format.py
'''

from pathlib import Path
from utils import conversion_kaist_tools
from utils import utilities
from utils import utilities


# Path to the images and annotations
kaist_path = Path('data/kaist_pedestrian/')
annotations_dir = kaist_path / 'annotations-vbb'
_outputdir = kaist_path / "converted_annotations"  

if not annotations_dir.exists():
    print(f"\n[INFO] vbb annotations not found...")
    print(f"[INFO] Downloading annotations...")

    try:
        os.makedirs(annotations_dir)
        os.system( 'curl -O http://multispectral.kaist.ac.kr/pedestrian/data-kaist/annotations-vbb.zip')
        os.system( 'unzip -d %s/annotations-vbb -q annotations-vbb.zip' % kaist_path )
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print(f"[ERROR] Downloading annotations failed.")
        exit(1)

# convert kaist to coco format
print(f"\n[INFO] Converting kaist to coco format...")
parsed_annotations = conversion_kaist_tools.convert_kaist_to_coco(annotations_dir)  
print(f"\n[INFO] Converting kaist to coco format completed.")

# # save the json file
utilities.save_json(data=parsed_annotations, 
                    save_dir=str(_outputdir),
                    file_name="kaist_converted_to_coco_format.json")  