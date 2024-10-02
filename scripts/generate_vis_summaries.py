# %% [markdown]
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

# %%
# expose parent directory to import modules
import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'vision-datasets-stats':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)

# %%
TASK='VIS'

# %% [markdown]
# ## **1. YTvis 2018 dataset**
# 
# ``` python
# 
# ## 1. YTvis dataset
# 
# from bases.youtube_vis_dataset import YoutubeVisDataset
# from pathlib import Path
# 
# dataset_year = 2019
# dataset_stem = f"ytvis_{dataset_year}"
# split = "train"
# subset = f"instances_{split}_sub"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = YoutubeVisDataset(annotation_file=str(annotiation_file))
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
# ## **2. SkyData dataset**
# 
# ``` python
# 
# ## 2. SkyData dataset
# 
# from bases.skydata_vis_dataset import SkyDataVis
# from pathlib import Path
# 
# dataset_year = ""
# dataset_stem = f"skydata{dataset_year}"
# split = "train"
# # subset = "train_SKYVIS_ds5_fr3_alldata"
# subset = f"{split}_SKYVIS_ds5_fr3_alldata"
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
# ## **3. YoutubeVis2021 dataset**
# 
# ``` python
# 
# ## 3. YoutubeVis2021 datase
# 
# 
# from bases.youtube_vis_dataset import YoutubeVisDataset
# from pathlib import Path
# 
# dataset_year = 2021
# dataset_stem = f"ytvis_{dataset_year}"
# split = "train"
# subset = f"instances_{split}_sub"
# annotiation_file = Path(f"./data/{dataset_stem}/annotations/{subset}.json")
# D = YoutubeVisDataset(annotation_file=str(annotiation_file))
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
# 
# ```

# %%



