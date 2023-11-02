
import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)



TASK='MOT'

##**5. TAO dataset**
from bases.tao_mot_coco import TAO
from pathlib import Path

dataset_year = ""
dataset_stem = f"tao{dataset_year}"
split = "train"
subset = f"{split}_with_freeform"
annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
D = TAO(annotation_file=str(annotiation_file))

# generate and load stats
D.generate_dataset_statistics()

# save the stats
D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
                            dataset_name = f"{dataset_stem}",
                            file_name = f"{subset}_stats.json"
                            )
print(f"[INFO] Saved")