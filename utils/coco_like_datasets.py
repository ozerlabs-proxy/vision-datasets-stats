
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
    
    #images stats
    stats["_images_stats"] = get_image_stats(D.dataset["images"])
    stats["images_count"] = stats["_images_stats"]["images_count"] if "images_count" in stats["_images_stats"] else 0


    #category stats 
    stats["_categories_stats"] = get_categories_stats(D.dataset)
    stats["categories_count"] = stats["_categories_stats"]["categories_count"] if "categories_count" in stats["_categories_stats"] else 0

    #super categories stats
    stats["_super_categories_stats"] = get_super_categories_stats( D.dataset["categories"])

    #annotations stats
    stats["annotations_count"] = len(list(set([ann["id"] for ann in D.dataset["annotations"]])))

    # bounding box stats
    stats["_boxes_stats"] = get_boxes_stats(D.dataset["annotations"])
    # masks stats
    stats["_masks_stats"] = get_masks_stats(D.dataset["annotations"])

    return stats

"""
--------------Helper functions-----------------
"""

def get_categories_stats(dataset):
    """
    given categories generate categories related insights

    """
    categories = dataset["categories"]
    categories_stats = {
        "_is_categories": False
    }
    if type(categories) == list and len(categories) == 0:
        return categories_stats
    assert len(categories) > 0, "categories should not be empty"

    _ids_to_categories=({int(cat["id"]): cat["name"] for cat in categories})
    categories_stats={
                    "_is_categories": True,
                    "categories" : _ids_to_categories,
                    "categories_count": len(list(_ids_to_categories.keys())),
                    "per_category_stats": get_per_category_stats(dataset)                
                        }
    return categories_stats

def get_masks_stats(annotations : list[dict] = []):
    """
    given annotations generate masks related insights

    """
    masks_stats = {
        "_is_masks": False
    }
    if type(annotations) == list and len(annotations) == 0:
        return masks_stats 
    assert len(annotations) > 0, "annotations should not be empty"
    if "segmentation" not in annotations[0] or len(annotations[0]["segmentation"]) == 0:
        return masks_stats

    masks = [ann["segmentation"] for ann in annotations]
    
    masks_stats = {
        "_is_masks": True,
        "masks_count": len(masks)
                }
    return masks_stats

def get_boxes_stats(annotations : list[dict] = []):
        """
        given annotations generate bounding boxes related insights
        """

        boxes_stats = {}

        if type(annotations) == list and len(annotations) == 0:
            return {}
        assert len(annotations) > 0, "annotations should not be empty"
        if "bbox" not in annotations[0]:
            return {}

        boxes = np.asarray([ann["bbox"] for ann in annotations])
        boxes_areas = np.asarray([float(ann["area"]) for ann in annotations])
        boxes_ratios = np.asarray([np.finfo(np.float32).eps if ann["bbox"][3]==0 else (ann["bbox"][2] / float(ann["bbox"][3])) for ann in annotations])

        # box_ratios histogram
        BINS = 100
        boxes_ratios_hist, boxes_ratios_bins = np.histogram(boxes_ratios, bins=BINS)

        # areas histogram
        boxes_areas_hist, boxes_areas_bins = np.histogram(boxes_areas, bins=BINS)

        # coco and/or skydata areas sizes stats 
        _ranges_sizes = {'Micro':12**2, 
                        'Tiny':22**2,
                        'Small':32**2, 
                        'Medium':96**2, 
                        'Large':np.inf}
        boundaries = [0,*list(_ranges_sizes.values())]
        per_bin_counts , boundaries= np.histogram(boxes_areas, bins=boundaries)

        _area_ranges_stats = {str(k):v for k,v in zip(_ranges_sizes.keys(), per_bin_counts)}
        
        boxes_stats = {
            "_is_bboxes": True,
            "areas_stats": {
                "min": np.min(boxes_areas),
                "max": np.max(boxes_areas),
                "mean": np.mean(boxes_areas),
                "std": np.std(boxes_areas),
                "median": np.median(boxes_areas)
            },
            "ratios_stats": {
                "min": np.min(boxes_ratios),
                "max": np.max(boxes_ratios),
                "mean": np.mean(boxes_ratios),
                "std": np.std(boxes_ratios),
                "median": np.median(boxes_ratios)
            },
            "ratios_hist": {
                "bins": BINS,
                "bins_bounds": boxes_ratios_bins.tolist(),
                "hist": boxes_ratios_hist.tolist()
            },
            "areas_hist": {
                "bins": BINS,
                "bins_bounds": boxes_areas_bins.tolist(),
                "hist": boxes_areas_hist.tolist()
            },
            "areas_ranges": _ranges_sizes,
            "areas_ranges_stats": _area_ranges_stats
        }
        return boxes_stats

def get_super_categories_stats(categories : list[dict] = []):
    """
    Get the super categories's insights from categories
    """
    super_categories = []
    super_categories_stats = {}
    for cat in categories:
        if "supercategory" in cat:
            super_categories.append(cat["supercategory"])

    super_categories_stats={
        "super_categories" : list(set(super_categories)),
        "super_categories_count": len(list(set(super_categories))),
        "is_super_categories":len(super_categories) > 0
    }
    return super_categories_stats

def get_per_category_stats(dataset):
    """
    Given a dataset, return the number of annotations per category.
    """
    catToImgs = defaultdict(list)
    if 'annotations' in dataset and 'categories' in dataset:
        for ann in dataset['annotations']:
            catToImgs[int(ann['category_id'])].append(int(ann['image_id']))

    per_category_stats= {}

    categories=({int(cat["id"]): cat["name"] for cat in dataset["categories"]})

    for k,v in catToImgs.items():
        if int(k) in categories:
            per_category_stats.update({categories[k]:len(v)})
        else:
            per_category_stats.update({k:len(v)})
    
    return per_category_stats

def get_image_stats(images : list[dict] = []):  
    """
    Given a list of images, return the number of images, the minimum and maximum resolution in the dataset.
    Args:
        images: list of image dictionaries
    Returns:
        _img_counts: number of images in the dataset
        _img_res_min: minimum resolution in the dataset
        _img_res_max: maximum resolution in the dataset
    Usage:
        _img_counts, _img_res_min, _img_res_max = get_image_stats(images)

    """     
    images_stats = {
        "images_count": 0,
        }
    if type(images) == list and len(images) == 0:
        return images_stats
    assert len(images) > 0, "images should not be empty"

    _img_counts = len(list(set([img["id"] for img in images])))
    resolutions_products = np.asarray([int(img["width"]) * int(img["height"]) for img in images])
    _img_res_min_index = np.argmin(np.asarray(resolutions_products).squeeze())
    _img_res_max_index = np.argmax(np.asarray(resolutions_products).squeeze())
    _img_res_min = (images[_img_res_min_index]["width"], images[_img_res_min_index]["height"])
    _img_res_max = (images[_img_res_max_index]["width"], images[_img_res_max_index]["height"])
    

    images_stats["images_count"] = int(_img_counts)
    images_stats["min_resolution"] = f"{_img_res_min[0]} x {_img_res_min[1]}"
    images_stats["max_resolution"] = f"{_img_res_max[0]} x {_img_res_max[1]}"

    return images_stats