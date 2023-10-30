# ## [markdown]
# # Tracking Datasets
# 
# All dataset will have classes that read annotations. The dataset class needs to extend our custom `BaseDatasetTracking` class. 
# 
# The `BaseDatasetTracking` class has the following methods:
# 
# * `generate_dataset_statistics`: generates a summary of the dataset (e.g. number of videos, number of annotations, etc.)
# * `save_dataset_statistics`: saves the summary to a `json` file
# 
# 
# 

# ##
# expose parent directory to import modules
import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)

# ##
TASK='Tracking'

# ## [markdown]
# ## **1. YTvis dataset**
# 
# ``` python
# 
# ```

# ##

## 1. YTvis dataset

from bases.youtube_vis_dataset import YoutubeVisDataset
from pathlib import Path

dataset_year = 2019
dataset_stem = f"ytvis_{dataset_year}"
split = "train"
subset = f"instances_{split}_sub"
annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
D = YoutubeVisDataset(annotation_file=str(annotiation_file))

# generate and load stats
D.generate_dataset_statistics()

xD = D 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"coco{coco_year}",
#                             file_name = f"{subset}_stats.json"
#                             )



