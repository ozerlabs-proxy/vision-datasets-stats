# %% [markdown]
# # 1. Detection-stats
# 
# To generate stats, we will read the summary files for different datasets in `summary folder`. The summary folder contains folders named after the dataset name. Each dataset folder contains summary files extacted by respective scripts. The summary files are in json format. We will read the json files and generate stats.
# 
# We will generate per dataset stats and general stats combining all the datasets.
# 
# Among the stats, we will generate the following:
# 
# * [ ] 1. Number of images `all_ds`
# * [ ] 2. Number of objects `all_ds`
# * [ ] 3. Number of classes `all_ds`
# * [ ] 4. Number of instances per class `per_ds` 
# * [ ] 5. Average number of instances per image `all_ds` 
# <!-- * [ ] 6. Bounding box area distribution `all_ds` -->
# 
# 
# The results will be saved in summaries in respective dataset folders.

# %%
# expose parent directory to import modules
import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)

TASK = 'detection'

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

global_summary_plain_value_cols_df = pd.DataFrame()
global_summary_images_stats = pd.DataFrame()
global_summary_masks_stats = pd.DataFrame()
global_areas_ranges_stats = defaultdict(list)
global_areas_ratios_general_stats = defaultdict(list)

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
    plain_value_cols_df=pd.DataFrame(plain_value_cols, index=[0])
    global_summary_plain_value_cols_df=stats_tools.merge_df(df1=global_summary_plain_value_cols_df, 
                                                            df2=plain_value_cols_df)
    
    #summarize _categories_stats for each dataset
    stats_tools.summarize_category_stats(dataset_name=dataset_name,
                                         _categories_stats = summary['_categories_stats'],
                                         save_path=summaries_path)
    
    # summarize_images_stats
    _images_stats_df = pd.DataFrame({"dataset_name":dataset_name, **summary['_images_stats']}, index=[0])
    global_summary_images_stats=stats_tools.merge_df(df1=global_summary_images_stats, 
                                                            df2=_images_stats_df)
    
    # summarize _masks_stats
    _masks_stats_df = pd.DataFrame({"dataset_name":dataset_name, **summary['_masks_stats']}, index=[0])
    global_summary_masks_stats=stats_tools.merge_df(df1=global_summary_masks_stats, 
                                                            df2=_masks_stats_df)

    ##skydata/coco sizes boxes boxes stats
    # 
    boxes_stats=summary['_boxes_stats']
    areas_ranges_stats=boxes_stats['areas_ranges_stats']

    global_areas_ranges_stats["dataset_name"].append(dataset_name)
    [global_areas_ranges_stats[k].append(v) for k,v in areas_ranges_stats.items()]

    ## per datasets ratios stats
    _ratios={"dataset_name":dataset_name, 
             "ratios_hist":summary['_boxes_stats']['ratios_hist']}
    stats_tools.plot_save_per_dataset_ratios_hist(_ratios=_ratios,
                                                    save_path=summaries_path/dataset_name/'plots',
                                                    file_name=f'{dataset_name}_ratios_hist')
    
    ## global ratios and areas stats
    #_is_bboxes, areas_stats, ratios_stats,areas_ranges
    _area_ratio_stats=stats_tools.get_formated_area_stats_per_dataset(dataset_name=dataset_name, 
                                                    boxes_stats=boxes_stats)
    [global_areas_ratios_general_stats[k].append(v) for k,v in _area_ratio_stats.items()]
    

# %%
# plot generals and save stats

## global_summary_plain_value_cols_df save to csv
stats_tools.save_df_to_csv(df=global_summary_plain_value_cols_df,
                            save_path=summaries_path/'all_datasets',
                            file_name='_plain_value_global.csv')


## global_summary_images_stats save to csv
stats_tools.summarize_global_images_plot_and_save(global_summary_images_stats=global_summary_images_stats,
                                                  save_path=summaries_path/'all_datasets',
                                                  file_name='_images_stats_global')

## global_summary_masks_stats save to csv
stats_tools.summarize_global_summary_masks_stats_plot_and_save(global_summary_masks_stats=global_summary_masks_stats,
                                                  save_path=summaries_path/'all_datasets',
                                                  file_name='_masks_stats_global')

# ## global_areas_ranges_stats save to csv
stats_tools.summarize_global_areas_ranges_stats_plot_and_save(global_areas_ranges_stats_df=global_areas_ranges_stats,
                                                  save_path=summaries_path/'all_datasets',
                                                  file_name='_areas_ranges_stats_global')

# ## global_areas_ratios_general_stats save to csv
stats_tools.summarize_global_areas_ratios_general_stats_plot_and_save(stats=global_areas_ratios_general_stats,
                                                                    save_path=summaries_path/'all_datasets',
                                                                    file_name='_areas_ratios_general_stats')


