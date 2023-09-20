
from bases.base_dataset_functionality import BaseDataset
from collections import defaultdict
import numpy as np


def generate_stats_coco_like(D:BaseDataset) -> dict:

    """
        Generate statistics for coco like datasets.  

        Args:
            D: dataset object
        Returns:
            stats: dictionary of statistics
        
        attributes:
            info: info about the dataset
            images_count: # of images in the dataset
            annotations_count: #of annotations(objects)
            categories_count: #of categories in the dataset
            categories: list of all categories in the dataset
            is_super_categories: True if the dataset contains super categories annotations
            super_categories: list of all super categories in the dataset
            is_bboxes: True if the dataset contains bounding boxes annotations
            is_masks: True if the dataset contains masks annotations
            bbox_areas_stats: statistics about the bounding boxes areas
            per_category_stats: statistics about the annotations per category
        Usage:
            stats = generate_stats_coco_like(D)
    """

    stats = defaultdict(dict)

    #info 
    stats["info"] = D.dataset["info"]

    #images count
    stats["images_count"] = len(list(set([img["id"] for img in D.dataset["images"]])))

    #annotations count
    stats["annotations_count"] = len(list(set([ann["id"] for ann in D.dataset["annotations"]])))

    ######## category stats ########
    #categories count
    stats["categories_count"] = len(list(set([cat["id"] for cat in D.dataset["categories"]])))

    #categories ids
    categories=({int(cat["id"]): cat["name"] for cat in D.dataset["categories"]})
    stats["categories"] =categories

    #super categories count
    super_categories = []
    for cat in D.dataset["categories"]:
        if "supercategory" in cat:
            super_categories.append(cat["supercategory"])

    stats["super_categories"] = list(set(super_categories))

    #super categories count
    stats["super_categories_count"] = len(list(set(super_categories)))

    # is_supercategory 
    stats["_is_super_categories"] = len(super_categories) > 0

    # per category stats
    catToImgs = defaultdict(list)
    if 'annotations' in D.dataset and 'categories' in D.dataset:
        for ann in D.dataset['annotations']:
            catToImgs[int(ann['category_id'])].append(int(ann['image_id']))
    stats["per_category_stats"]= {}
    for k,v in catToImgs.items():
        if k in categories:
            stats["per_category_stats"].update({categories[k]:len(v)})
        else:
            stats["per_category_stats"].update({k:len(v)})


    stats["_is_bboxes"] = "bbox" in D.dataset["annotations"][0]

    # bounding box stats
    bbox_areas = np.array([ann["area"] for ann in D.dataset["annotations"]])
    stats["bbox_areas_stats"] = {"min": np.min(bbox_areas),
                        "max": np.max(bbox_areas),
                        "mean": np.mean(bbox_areas),
                        "std": np.std(bbox_areas),
                        "median": np.median(bbox_areas)
    }

    stats["_is_masks"] = "segmentation" in D.dataset["annotations"][0]

    return stats
