# %% [markdown]
# # 1. VIS-stats
# generate video instance segmentation (VIS) stats for a video datasets
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

TASK = 'VIS'

# %%


# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from pathlib import Path
import json
import warnings
from collections import defaultdict
sns.set()

from utils import stats_tools
warnings.filterwarnings('ignore')

# %%
#

summaries_path = Path('./summaries')
summaries_path= summaries_path / TASK
summaries_path.mkdir(parents=True, exist_ok=True)

# %%
# get dataset to file paths
dataset_to_file_paths = stats_tools.get_dataset_to_file_paths(str(summaries_path))

# len(dataset_to_file_paths), dataset_to_file_paths

# %%
dataset_to_file_paths

# %%

global_summary_plain_value_cols_df = pd.DataFrame()
global_summary_videos_stats = pd.DataFrame()
global_areas_ranges_stats = defaultdict(list)
global_tracks_stats = defaultdict(list)

for dataset_name, file_path in dataset_to_file_paths.items():
    
    print("*"*20 + f"{dataset_name}" + "*"*20)
    # load data
    summary = stats_tools.load_summary(file_path=file_path)
    dataset_to_summary = {dataset_name: summary}

    # plain-common-stats-stats-plots-save
    all_columns = list(summary.keys())
    plain_value_cols = {}
    plain_value_cols["dataset_name"] = dataset_name
    plain_value_cols.update({ k:v for (k,v) in summary.items() if not isinstance(summary[k], (list, dict))})
    plain_value_cols.update(summary['info'])
    plain_value_cols.update(summary['_general_stats'])
    plain_value_cols.update(summary['tracks_stats'])
    plain_value_cols.update({
                        'categories_count': summary['_cats']["categories_count"],
                        'super_categories_count': summary['_cats']["super_categories_count"]
                        })
    
    plain_value_cols_df=pd.DataFrame(plain_value_cols, index=[0])
    global_summary_plain_value_cols_df=stats_tools.merge_df(df1=global_summary_plain_value_cols_df, 
                                                            df2=plain_value_cols_df)
    
    #summarize _categories_stats for each dataset
    stats_tools.plot_and_save_per_category_stats(per_category_stats = summary["_categories_stats"],
                                                    dataset_name = dataset_name, 
                                                    save_path = summaries_path)

    ##skydata/coco sizes boxes boxes stats
    # 
    boxes_stats=summary['_areas_stats']
    areas_ranges_stats=boxes_stats['areas_stats']

    global_areas_ranges_stats["dataset_name"].append(dataset_name)
    [global_areas_ranges_stats[k].append(v) for k,v in areas_ranges_stats.items()]
    

    # # summarize tracks
    tracks_stats = summary['tracks_stats']
    global_tracks_stats["dataset_name"].append(dataset_name)
    [global_tracks_stats[k].append(v) for k,v in tracks_stats.items()]
    

    

# %%
# plot generals and save stats

## global_summary_plain_value_cols_df save to csv
stats_tools.save_df_to_csv(df=global_summary_plain_value_cols_df,
                            save_path=summaries_path/'all_datasets',
                            file_name='_plain_value_global.csv')

# ## global_areas_ranges_stats save to csv
stats_tools.summarize_global_areas_ranges_stats_plot_and_save(global_areas_ranges_stats_df=global_areas_ranges_stats,
                                                    save_path=summaries_path/'all_datasets',
                                                    file_name='_areas_ranges_stats_global')


# ## global_tracks_stats save to csv
stats_tools.summarize_global_tracks_stats_plot_and_save(global_tracks_stats_df=global_tracks_stats,
                                                    save_path=summaries_path/'all_datasets',
                                                    file_name='_tracks_stats_global')

# %%


# %%



