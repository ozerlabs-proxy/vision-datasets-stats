# %% [markdown]
# # Multiple Object Tracking  Datasets
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

# %%
# expose parent directory to import modules
import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)

# %%
TASK='MOT'

# %% [markdown]
# ## **1. MOT 2017 dataset**
# 
# ``` python
# 
# ## 1. MOT 2017 dataset
# from bases.mot_coco import MOT_IN_COCO
# from pathlib import Path
# 
# dataset_year = 2017
# dataset_stem = f"MOT{dataset_year}"
# split = "train"
# subset = f"{split}_cocoformat"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = MOT_IN_COCO(annotation_file=str(annotiation_file))
# 
# # # generate and load stats
# D.generate_dataset_statistics()
# 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"{dataset_stem}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print(f"[INFO] Saved")
# 
# ```

# %% [markdown]
# ## **2. MOT 2020 dataset**
# 
# ``` python
# 
# ## 2. MOT 2020 dataset
# from bases.mot_coco import MOT_IN_COCO
# from pathlib import Path
# 
# dataset_year = 2020
# dataset_stem = f"MOT{dataset_year}"
# split = "train"
# subset = f"{split}_cocoformat"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = MOT_IN_COCO(annotation_file=str(annotiation_file))
# 
# # # generate and load stats
# D.generate_dataset_statistics()
# 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"{dataset_stem}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print(f"[INFO] Saved")
# 
# ```

# %% [markdown]
# ## **3.  Visdrone MOT dataset**
# 
# ``` python
# 
# ## 3. Visdrone MOT dataset
# from bases.visdrone_mot import VisDroneMOT 
# from pathlib import Path
# 
# tag = "mot"
# dataset_stem = f"visdrone_{tag}"
# split = "visdrone_mot"
# subset = f"{split}_cocoformat" 
# annotiation_file = Path(f"./data/{dataset_stem}/converted_annotations/{subset}.json")
# D = VisDroneMOT(annotation_file=str(annotiation_file))
# 
# # # generate and load stats
# D.generate_dataset_statistics()
# 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"{dataset_stem}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print(f"[INFO] Saved")
# 
# ```

# %% [markdown]
# ## **4.  SKYDATA MOT dataset**
# 
# ``` python
# 
# ## 4.  SKYDATA MOT dataset
# 
# # ##
# TASK='MOT'
# 
# ## 4. SKYDATA MOT dataset
# from bases.skydata_vis_dataset import SkyDataVis
# from pathlib import Path
# 
# dataset_year = ""
# dataset_stem = f"skydata{dataset_year}"
# split = "train"
# # subset = "train_SKYVIS_ds5_fr3_alldata"
# # "data/skydata/annotations/train_SKYVIS_3_alldata.json"
# subset = f"{split}_SKYVIS_3_alldata"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = SkyDataVis(annotation_file=str(annotiation_file))
# 
# # generate and load stats
# D.generate_dataset_statistics()
# 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"{dataset_stem}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print(f"[INFO] Saved")
# 
# ```

# %% [markdown]
# ## **5. DanceTRack dataset**
# 
# ``` python
# ## **5. DanceTRack dataset**
# 
# # ##
# TASK='MOT'
# 
# ##**5. DanceTRack dataset**
# from bases.dancetrack_coco import DanceTrack
# from pathlib import Path
# 
# dataset_year = ""
# dataset_stem = f"DanceTrack{dataset_year}"
# split = "train"
# subset = f"{split}_cocoformat"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = DanceTrack(annotation_file=str(annotiation_file))
# 
# # generate and load stats
# D.generate_dataset_statistics()
# 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"{dataset_stem}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print(f"[INFO] Saved")
# 
# ```

# %% [markdown]
# ## **6. TAO dataset**
# 
# ``` python
# ## **6. TAO dataset**
# 
# # ##
# TASK='MOT'
# 
# ##**5. TAO dataset**
# from bases.dancetrack_coco import DanceTrack
# from pathlib import Path
# 
# dataset_year = ""
# dataset_stem = f"tao{dataset_year}"
# split = "train"
# subset = f"{split}_with_freeform"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = DanceTrack(annotation_file=str(annotiation_file))
# 
# # generate and load stats
# D.generate_dataset_statistics()
# 
# # save the stats
# D.save_dataset_statistics(save_path = f"./summaries/{TASK}",
#                             dataset_name = f"{dataset_stem}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print(f"[INFO] Saved")
# 
# ```

# %%
## **6. TAO dataset**

# ##
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

# %%



