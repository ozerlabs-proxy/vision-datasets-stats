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
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

#************** BOXES stats ******************#
#_is_bboxes, areas_stats, ratios_stats,areas_ranges


def summarize_global_areas_ratios_general_stats_plot_and_save(stats,
                                                                save_path,
                                                                file_name):
    """
    Accepts ratios and areas  and saves it as csv and plots it
    """
    # save global_areas_ranges_stats_d    
    print(f"[INFO] General ratios and areas stats ....")
    save_path = Path(save_path)
    stats=pd.DataFrame(stats)

    #plot possible plots for areas and ratios
    old_stats = stats.copy()
    stats = stats.drop(columns=[str(col) for col in stats.columns if 'max' in str(col)])
    stats.plot(x='dataset_name',   
                    #   y=[
                    #      'mean_area', 
                    #      'median_area', 
                    #      'std_area', 
                    #      'min_area', 
                    #      'mean_ratio',
                    #      ],                                       
                    kind='bar', 
                    figsize=(15,15),
                    title="box ratios and areas Stats",
                    xlabel="")

    plt.xticks(rotation=90)
    plt.savefig(str(save_path/f'{file_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()

    save_df_to_csv(df=old_stats,
                    save_path=save_path,
                    file_name=f'{file_name}.csv')



def get_formated_area_stats_per_dataset(dataset_name:str, 
                                                boxes_stats:dict):
    """
    Given boxes_stats, return a dictionary containing the area stats per dataset
    """
    summary = {"dataset_name": dataset_name,
               "_is_bboxes":  boxes_stats['_is_bboxes'],
               **{f'{k}_area':round(v, 2) if type(v) is float else v for k,v in boxes_stats['areas_stats'].items()},
               **{f'{k}':round(v, 2) if type(v) is float else v for k,v in boxes_stats['areas_ranges_stats'].items()},
               **{f'{k}_ratio':round(v, 2) if type(v) is float else v for k,v in boxes_stats['ratios_stats'].items()},
               }

    return summary

def plot_save_per_dataset_ratios_hist(_ratios,
                                      save_path,
                                      file_name='ratios_hist'):
    
    '''
    Given ratios per dataset, plot and save ratios hist
    '''
    print(f"[INFO] per dataset ratios stats ....")
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Saving...")
    _dataset_name = _ratios['dataset_name']
    # _bins_count = _ratios['ratios_hist']['bins']
    _ratios_bins = _ratios['ratios_hist']['bins_bounds'][1:]
    _ratios_values = _ratios['ratios_hist']['hist'] / np.sum(_ratios['ratios_hist']['hist'])

    # plot ratios hist
    plt.figure(figsize=(10,5))
    plt.bar(_ratios_bins, _ratios_values, width=0.2, color='b', align='center')
    plt.title(f"{_dataset_name} ratios distribution")
    plt.xlabel("ratios")
    plt.ylabel("%",loc='top')
    plt.xlim(np.min(_ratios_bins)-1, np.max(_ratios_bins))
    plt.ylim(0, np.max(_ratios_values)+0.1)
    # plt.xticks(rotation=90)
    plt.savefig(str(save_path/f'{file_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[INFO] Saved.")


def summarize_global_tracks_stats_plot_and_save(global_tracks_stats_df,
                                                  save_path,
                                                  file_name):
    
    
    '''
    Given tracks stats, plot and save tracks stats
    '''
    print(f"[INFO] Global tracks stats ....")
    save_path = Path(save_path)
    global_tracks_stats_df=pd.DataFrame(global_tracks_stats_df)

    global_tracks_stats_df.plot.bar(x='dataset_name',
                                            figsize=(15,10),
                                            title='(instances) tracks_stats',
                                            xlabel="",
                                            )
    plt.xticks(rotation=90)
    plt.savefig(str(save_path/f'{file_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()

    save_df_to_csv(df=global_tracks_stats_df,
                                save_path=save_path,
                                file_name=f'{file_name}.csv')
    
    

def summarize_global_areas_ranges_stats_plot_and_save(global_areas_ranges_stats_df,
                                                  save_path,
                                                  file_name):
    """
    Accepts global_areas_ranges_stats_df and saves it as csv and plots it
    """
    # save global_areas_ranges_stats_d    
    print(f"[INFO] Global areas stats ....")
    save_path = Path(save_path)
    global_areas_ranges_stats_df=pd.DataFrame(global_areas_ranges_stats_df)

    # # plot areas_ranges_stats on the same plot
    # fig, ax = plt.subplots(figsize=(10, 10))
    # for col in global_areas_ranges_stats_df.columns[1:]:
    #     ax.scatter(global_areas_ranges_stats_df['dataset_name'], 
    #             global_areas_ranges_stats_df[col], 
    #             label=col,
    #             alpha=0.8,
    #             s=global_areas_ranges_stats_df[col]*.001 if global_areas_ranges_stats_df[col].median() > 10000 else global_areas_ranges_stats_df[col])
    # ax.legend()
    global_areas_ranges_stats_df.plot.bar(x='dataset_name',
                                            figsize=(15,10),
                                            title='areas_ranges_stats',
                                            xlabel="",
                                            
                                            )
    plt.xticks(rotation=90)
    plt.savefig(str(save_path/f'{file_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()

    save_df_to_csv(df=global_areas_ranges_stats_df,
                                save_path=save_path,
                                file_name=f'{file_name}.csv')

#************** masks stats ******************#

def summarize_global_summary_masks_stats_plot_and_save(global_summary_masks_stats,
                                                  save_path,
                                                  file_name):

    """
    summarize global masks stats function
    """
    print(f"[INFO] Global images stats ....")
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    global_summary_masks_stats.plot(kind='bar', 
                                    figsize=(15,10), 
                                    x='dataset_name',
                                    title='images_stats',
                                    xlabel="",
                                    )
    plt.savefig(str(save_path/f'{file_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()

    save_df_to_csv(df=global_summary_masks_stats,
                                save_path=save_path,
                                file_name=f'{file_name}.csv')

#************** images stats ******************#
def summarize_global_images_plot_and_save(global_summary_images_stats,
                                          save_path,
                                          file_name):
    """
    summarize global images stats function
    """

    print(f"[INFO] Global images stats ....")
    save_path = Path(save_path)
    save_path.mkdir(parents=True, exist_ok=True)
    global_summary_images_stats.plot(kind='bar', 
                                    figsize=(15,10), 
                                    x='dataset_name',
                                    title='images_stats',
                                    xlabel="",
                                    )
    # annotate with resolutions and number of images
    for i, row in global_summary_images_stats.iterrows():
        plt.annotate(f"{row['images_count']}\n{row['min_resolution']}\n{row['max_resolution']}", 
                        xy=(i, row['images_count']), 
                        xytext=(i-0.26, row['images_count']+1000),
                        color='red',
                        size=8,
                        )

    plt.savefig(str(save_path/f'{file_name}.png'), dpi=300, bbox_inches='tight')
    plt.close()

    save_df_to_csv(df=global_summary_images_stats,
                                save_path=save_path,
                                file_name=f'{file_name}.csv')

#************** Category stats ******************#    
def summarize_category_stats(dataset_name,
                            _categories_stats,
                            save_path):
    """
    summarize category stats function
    """

    
    print(f"[INFO] Category stats ....")
    per_category_stats = _categories_stats['per_category_stats']
    plot_and_save_per_category_stats(per_category_stats=per_category_stats, 
                                    dataset_name=dataset_name, 
                                    save_path=save_path)
    
def plot_and_save_per_category_stats(per_category_stats,
                                     dataset_name, 
                                     save_path = "summaries"):
    
    """
    plot and save category stats function
    """
    save_path = Path(save_path)/dataset_name/"plots"
    save_path.mkdir(parents=True, exist_ok=True)
    csv_save_path = save_path/f"{dataset_name}_per_category_stats.csv"
    save_path = save_path/f"{dataset_name}_per_category_stats.png"
    # convert to dataframe
    print(f"[INFO] saving plot ....")
    try:
        # per_category_stats_df = pd.DataFrame(per_category_stats)
        per_category_stats_df = pd.DataFrame(per_category_stats, index=[0])
    except:
        per_category_stats_df = pd.DataFrame(per_category_stats)
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
    
    # save to csv
    print(f"[INFO] saving csv ....")
    try:
        save_df_to_csv(per_category_stats_df,
                            save_path=str(csv_save_path.parent),
                            file_name=str(csv_save_path.name))
    except Exception as e:
        # print(e)
        print(f"[ERROR] could not save {csv_save_path}")
        
    print(f"[INFO] Saved.")


#************** General Helper funcs ******************#

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
