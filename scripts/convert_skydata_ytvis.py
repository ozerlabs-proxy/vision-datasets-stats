
# expose parent directory to import modules
import os
import sys

print(f"[INFO] conversion will start now")

ROOT_DIR = os.getcwd()
while os.path.basename(ROOT_DIR) != 'DatasetsStatistics':
    ROOT_DIR = os.path.abspath(os.path.join(ROOT_DIR,'..'))
sys.path.insert(0,ROOT_DIR)
os.chdir(ROOT_DIR)



import json
import utils.utilities as common_utils
from pathlib import Path
from  tqdm import tqdm


##
print(f"[INFO] ROOT_DIR: {ROOT_DIR}")
##


def read_data(fullpath):
    
    ##
    print(f"[INFO] loading data from {fullpath}")
    ##
    try:
        f = open(fullpath)
        data = json.load(f)
    except:
        print(f"[ERROR] cannot load data from {fullpath}")
        data = None
        exit(1)
        
    return data


def writeJSON(dictionary, filepath):
    ##
    print(f"[INFO] dumping data to {filepath}")
    ##
    with open(filepath, "w") as outfile:
        json.dump(dictionary, outfile)


skydata_file = "data/skydata/annotations/train_VID.json"
skydata = read_data(skydata_file)


# ytvos_file = "instances_train_sub.json"
# ytvos = read_data(ytvos_file)



skyvos = {}
skyvos['info'] = skydata['info']
skyvos['videos'] = []
skyvos['annotations'] = []

files_by_videos = {}

print(f"[INFO] videos")
for vid in skydata['videos']:
    key = vid['id']
    if key not in files_by_videos:
        files_by_videos[key] = []

print(f"[INFO] image ids")
image_id_to_video_id = {}


for im in skydata['images']:
    video_id = im['video_id']
    files_by_videos[video_id].append(im)
    image_id_to_video_id[im['id']] = video_id

for vid in skydata['videos']:

    new_vid = {}
    new_vid['id'] = vid['id']
    new_vid['width'] = vid['width']
    new_vid['height'] = vid['height']

    new_vid['file_names'] = []
    for im in files_by_videos[new_vid['id']]:
        new_vid['file_names'].append(im['file_name'])
        

    skyvos['videos'].append(new_vid)


print(f"[INFO] annotations")
annotations_by_videos_and_trackid = {}

for ann in skydata['annotations']:

    image_id = ann['image_id']
    video_id = image_id_to_video_id[image_id]
    track_id = ann['track_id']

    key = (video_id, track_id)

    if key in annotations_by_videos_and_trackid:
        annotations_by_videos_and_trackid[key].append(ann)
    else:
        annotations_by_videos_and_trackid[key] = [ann]

print(f"[INFO] image id to frame index")
image_id_to_frame_index = {}

for k,v in files_by_videos.items():
    for frame in v:
        image_id_to_frame_index[frame['id']] = frame['frame_id']




global_id_tracker = 0

for key, value in annotations_by_videos_and_trackid.items():

    video_id, track_id = key

    new_ann = {}
    new_ann['id'] = global_id_tracker
    new_ann['video_id'] = video_id
    new_ann['category_id'] = value[0]['category_id'] + 1  # correction for background class
    new_ann['segmentations'] = [None] * len(files_by_videos[video_id])
    new_ann['areas'] = [None] * len(files_by_videos[video_id])
    new_ann['bboxes'] = [None] * len(files_by_videos[video_id])
    new_ann['iscrowd'] = 0  # overwritten for now, actual: value[0]['iscrowd']

    for ann in value:
        frame_idx = image_id_to_frame_index[ann['image_id']]

        new_ann['segmentations'][frame_idx] = ann['segmentation']
        new_ann['areas'][frame_idx] = ann['area']
        new_ann['bboxes'][frame_idx] = ann['bbox']

    skyvos['annotations'].append(new_ann)

    global_id_tracker += 1

skyvos['categories'] = skydata['categories']
for i,cat in enumerate(skyvos['categories']):
    cat['id'] += 1  # correction for background class
    skyvos['categories'][i] = cat

## dowmsample and divide

# DOWNSAMPLE_RATIO = 30
# FRAME_COUNT = 3
# FRAME_LIMIT = -1

# new_videos = []

# global_video_id_tracker = 0

# new_video_id_start_points = {}

# print(f"[INFO] downsampling and dividing")

# for vid in tqdm(skyvos['videos']):
#     vid['file_names'] = vid['file_names'][0::DOWNSAMPLE_RATIO]
#     vid['file_names'] = vid['file_names'][0:FRAME_LIMIT]

#     if FRAME_COUNT > 0:
#         N = (len(vid['file_names']) // FRAME_COUNT) * FRAME_COUNT

#         new_video_id_start_points[vid['id']] = global_video_id_tracker

#         for idx in range(0,N,FRAME_COUNT):
#             new_vid = {}
#             new_vid['id'] = global_video_id_tracker
#             new_vid['width'] = vid['width']
#             new_vid['height'] = vid['height']
#             new_vid['file_names'] = vid['file_names'][idx:idx+FRAME_COUNT]

#             new_videos.append(new_vid)

#             global_video_id_tracker += 1

# if FRAME_COUNT > 0:
#     skyvos['videos'] = new_videos

# new_annotations = []

# global_annotation_id_tracker = 0

# for ann in skyvos['annotations']:
#     ann['segmentations'] = ann['segmentations'][0::DOWNSAMPLE_RATIO]
#     ann['areas'] = ann['areas'][0::DOWNSAMPLE_RATIO]
#     ann['bboxes'] = ann['bboxes'][0::DOWNSAMPLE_RATIO]

#     ann['segmentations'] = ann['segmentations'][0:FRAME_LIMIT]
#     ann['areas'] = ann['areas'][0:FRAME_LIMIT]
#     ann['bboxes'] = ann['bboxes'][0:FRAME_LIMIT]

#     if FRAME_COUNT > 0:

#         N = (len(ann['segmentations']) // FRAME_COUNT) * FRAME_COUNT

#         video_id = new_video_id_start_points[ann['video_id']]

#         for idx in range(0,N,FRAME_COUNT):

#             new_ann = {}
#             new_ann['id'] = global_annotation_id_tracker
#             new_ann['video_id'] = video_id
#             new_ann['category_id'] = ann['category_id']
#             new_ann['segmentations'] = ann['segmentations'][idx:idx+FRAME_COUNT]
#             new_ann['areas'] = ann['areas'][idx:idx + FRAME_COUNT]
#             new_ann['bboxes'] = ann['bboxes'][idx:idx + FRAME_COUNT]
#             new_ann['iscrowd'] = ann['iscrowd']

#             new_annotations.append(new_ann)

#             video_id += 1
#             global_annotation_id_tracker += 1

# if FRAME_COUNT > 0:
#     skyvos['annotations'] = new_annotations

print("annotation convert completed.")

common_utils.save_json(skyvos, 
                        "data/skydata/annotations",
                        "train_SKYVIS_3_alldata.json")

print("generation of json file complated.")

