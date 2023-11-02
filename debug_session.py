
import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)

# ##
TASK='MOT'

## 4. SKYDATA MOT dataset
from bases.skydata_vis_dataset import SkyDataVis
from pathlib import Path

dataset_year = ""
dataset_stem = f"skydata{dataset_year}"
split = "train"
# subset = "train_SKYVIS_ds5_fr3_alldata"
# "data/skydata/annotations/train_SKYVIS_3_alldata.json"
subset = f"{split}_SKYVIS_3_alldata"
annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
D = SkyDataVis(annotation_file=str(annotiation_file))

# generate and load stats
D.generate_dataset_statistics()

# save the stats
D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
                            dataset_name = f"{dataset_stem}",
                            file_name = f"{subset}_stats.json"
                            )
print(f"[INFO] Saved")