"""
write a script that run per task generate_stats.py and if necessary run generate_summaries.py
"""

GENERATE_STATS = True
GENERATE_SUMMARIES = False


import os
import sys

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)


"""
    SUMMARIES
    
    generate summaries for each task, then run generate statistics for each task
    
"""

summaries_scripts_per_task = {
    "detection": "generate_detection_summaries.py",
    "segmentation": "generate_segmentation_summaries.py",
    "vis": "generate_vis_summaries.py",
    "mot": "generate_mot_summaries.py"
}

if GENERATE_SUMMARIES:
    print(f"\n[INFO] Generating summaries...")
    
    for task, script in summaries_scripts_per_task.items():
        print(f"\n[INFO] {task} ...")
        
        try:
            os.system(f"conda activate dsetStats")    
            os.system(f"python ./scripts/{script}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
            print(f"skipping {task}.")
            continue
        print(f"*"*50)
        
    print(f"\n[INFO] Generating summaries completed.")
    
    
"""
    STATS
    
    generate stats for the tasks that have summaries
"""


stats_scripts_per_task = {
    "detection": "generate_detection_stats.py",
    "segmentation": "generate_segmentation_stats.py",
    "vis": "generate_vis_stats.py",
    "mot": "generate_mot_stats.py"
}

if GENERATE_STATS:
    
    print(f"\n[INFO] Generating stats...")
    
    for task, script in stats_scripts_per_task.items():
        print(f"\n[INFO] {task} ...")
        
        try:
            os.system(f"conda activate dsetStats")    
            os.system(f"python ./scripts/{script}")
        except Exception as e:
            print(f"\n[ERROR] {e}")
            print(f"skipping {task}.")
            continue
        print(f"*"*50)
        
    print(f"\n[INFO] Generating stats completed.")
    
    
print(f"\n[INFO] Done.")