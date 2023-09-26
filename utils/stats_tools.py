"""
will contain functions for dataset statistics. 

"""

import os
import sys
sys.path.append('../')

import json
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

def get_dataset_to_file_paths(summaries_path):
    """
    Given a path to the summaries directory, return a dictionary mapping dataset names to the path of their summary file.
    """
    # walk through all the files in the summaries directory
    dataset_to_file_paths = {}
    summaries_path = Path(summaries_path)
    summaries_path = list(summaries_path.glob('./*/*.json'))

    for files in summaries_path:
        parent_dir, summary_file = files.parent, files.name
        dataset_name = parent_dir.name
        # files = [f for f in files if f.endswith('.json')]
        assert summary_file.endswith('.json'), f"summary file must be a json file. {summary_file} is not a json file"
        dataset_to_file_paths[dataset_name] = Path(files)

    return dataset_to_file_paths

def load_summary(file_path):

    """
    Load a summary file
    """
    # load the summary file
    print(f"[INFO] Loading {file_path.name}")
    try:
        with open(file_path, 'r') as f:
            summary = json.load(f)
    except Exception as e:
        print(e)
        print(f"Could not load {file_path}")
    print(f"[INFO] Loaded {file_path.name}")
    # get the summary keys

    return summary


def merge_df(df1, df2):
    """
    merge two dataframes
    """
    try:
        df1 = df1.merge(df2, how='outer')
    except:
        df1 = pd.DataFrame(df2, index=[0])
    return df1

def save_df_to_csv(df,
                   save_path="summaries",
                    file_name="summary.csv"):
    """
    save dataframe to csv
    """

    assert isinstance(df, pd.DataFrame), "df must be a pandas dataframe"

    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Saving {save_path.name}")
    try:
        save_path = save_path/file_name
        df.to_csv(save_path, index=False)
    except Exception as e:
        print(f"Could not save {save_path}")

    print(f"[INFO] Saved {save_path.name}")
    

def plot_and_save_per_category_stats(per_category_stats,
                                     dataset_name, 
                                     save_path = "summaries"):
    
    """
    plot and save category stats function
    """


    save_path = Path(save_path)/dataset_name/"plots"
    save_path.mkdir(parents=True, exist_ok=True)
    save_path = save_path/f"{dataset_name}_per_category_stats.png"
    print(f"[INFO] Category stats ....")
    # convert to dataframe
    print(f"[INFO] saving plot ....")
    per_category_stats_df = pd.DataFrame(per_category_stats, index=[0])
    # plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title(f'{dataset_name} per category stats')
    ax.set_ylabel('Count')
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.barplot(data=per_category_stats_df, ax=ax)
    # plt.show()
    plt.savefig(save_path,dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved.")



