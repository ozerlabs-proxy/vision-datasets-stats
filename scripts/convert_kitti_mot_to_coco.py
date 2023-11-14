import functools
import json
import os
import random
import shutil
from collections import defaultdict

import matplotlib.pyplot as plt
import pycocotools
from pycocotools import mask
import numpy as np
import pandas as pd
import uuid
import cv2
from pprint import pprint

import itertools

from PIL import Image

LABEL_INTER_PATH = '/tmp/KITTI_label_crop'
# img translation: origin_size -> crop top 120 px ->  rescale to TARGET_IMG_SIZE
TARGET_IMG_SIZE = (1024, 256)

CROP_SIZE = 120

categories = set()
categories_dist = defaultdict(int)
fixed_category = {
    k: idx for idx, k in
    # list(zip([1, 0, 0, 3, 2, 0, 0, 4, 2],
    #          ['Cyclist', 'Van', 'Car', 'Misc', 'Pedestrian', 'Tram', 'Truck', 'DontCare', 'Person']))
    list(zip([0, 1, 2], ['Car', 'Van', 'Truck', ]))
}



def parse_label(path, img_id, width, height, task):
    """
    convert KITTI label to coco format
    :param path:
    :param img_id:
    :param width:
    :param height:
    :return: annotations
    """
    try:
        labels = pd.read_csv(path, delimiter=' ', header=None).values
    except Exception:
        print('Empty Label: {}'.format(path))
        return []
    annotations = []
    for idx, label in enumerate(labels):
        category_id = label[0] if task == 'instance' else (fixed_category[label[0]] + 1)
        top_x, top_y, bottom_x, bottom_y = label[1:5]
        area = label[5] if task == 'instance' else (bottom_x - top_x) * (bottom_y - top_y)
        annotations.append({
            'id': '{}_{}'.format(img_id, idx),
            'image_id': img_id,
            'category_id': category_id,
            'segmentation': {'counts': label[-1], 'size': tuple(label[6:8])} if task == 'instance' else None,
            'area': area,
            'bbox': [top_x, top_y, bottom_x - top_x, bottom_y - top_y],
            'iscrowd': 0,
        })
        categories.add(category_id)
    return annotations


def process_dataset(img_list, name, task):
    images = []
    annotations = []

    for idx, img_name in enumerate(sorted(img_list)):
        img_path = os.path.join(img_root, img_name)
        height, width = cv2.imread(img_path).shape[:2]
        img_name_wo_suffix = img_name[:img_name.rfind('.')].replace('/', '_')
        img_id = int(img_name_wo_suffix) if dataset_type == 'object' else int(img_name_wo_suffix.replace('_', ''))
        label_path = os.path.join(LABEL_INTER_PATH, '{}_{}.txt'.format(task, img_name_wo_suffix))

        # 解析标签
        annotation = parse_label(label_path, img_id=img_id, width=width, height=height, task=task)

        images.append({
            'license': 3,
            'file_name': img_name.replace('/', '_'),
            'width': TARGET_IMG_SIZE[0],
            'height': TARGET_IMG_SIZE[1],
            'id': img_id,
            'coco_url': '', 'date_captured': '', 'flickr_url': '',
        })
        annotations.extend(annotation)

        print('{}/{} {}'.format(idx, len(img_list), img_name))
        print(categories)

    dataset = {
        'info': {
            'description': 'KITTI Synthesis',
            'url': '',
            'version': '0.1',
            'year': 2020,
            'contributor': 'HVT@BDBC',
            'date_created': '2020/01/11'
        },
        'images': images,
        'annotations': annotations,
        "categories": [{
            "id": int(category_id),
            "name": str(category_id),
            "supercategory": 'str',
        } for category_id in categories]

    }

    json.dump(dataset, open(
        os.path.join(target_path, '{}_KITTI_{}_{}.json')
            .format(task, dataset_type, name), 'w'), indent=0)


if __name__ == '__main__':
    # KITTI_tracking_to_intermediate()
    # exit()

    # dataset_type = 'synthesised'
    dataset_type = 'tracking'
    # dataset_type = 'tracking'
    assert dataset_type in ['tracking', 'object', 'synthesised']

    dataset_root = '~/nalain-labs/Datasets/kitti_MOT/{}/training'.format(dataset_type)
    img_root = os.path.join(dataset_root, 'image_02' if dataset_type == 'tracking' else 'image_2')
    target_path = '~/nalain-labs/Datasets/kitti_MOT/real'

    if dataset_type == 'tracking':
        img_list = [[os.path.join(seq_root, img_path) for img_path in os.listdir(os.path.join(img_root, seq_root))]
                    for seq_root in os.listdir(img_root)]
        img_list = list(itertools.chain(*img_list))
    elif dataset_type == 'object':
        img_list = os.listdir(img_root)
    elif dataset_type == 'synthesised':
        img_list = [img for img in os.listdir(img_root)]
    else:
        raise NotImplementedError()

    random.shuffle(img_list)
    split = int(len(img_list) * 1)
    train_list = img_list[:split]
    process_dataset(train_list, 'train', task='detection')