# ## [markdown]
# **Visdrone annotations are in `text format`**
# 
# we are going to transform them into `json format` for further processing, and write a class to load the annotations. as we did in `coco` dataset.
# 
# the visdrone-det is structure as follows:
# 
# ```
#     VisDrone2019-DET-train/
#     ├── annotations
#     ├── images
# ```
# 
# in annotations, there are annotations in `txt` format, and in images, there are images in `jpg` format. each image has a corresponding annotation file that contains the bounding boxes of the objects in the image.

# ## [markdown]
# **Visdrone annotations Format**
# 
# ```
#  <bbox_left>,<bbox_top>,<bbox_width>,<bbox_height>,<score>,<object_category>,<truncation>,<occlusion>
# 
# 
#     Name                                                  Description
# -------------------------------------------------------------------------------------------------------------------------------     
#  <bbox_left>	     The x coordinate of the top-left corner of the predicted bounding box
# 
#  <bbox_top>	     The y coordinate of the top-left corner of the predicted object bounding box
# 
#  <bbox_width>	     The width in pixels of the predicted object bounding box
# 
# <bbox_height>	     The height in pixels of the predicted object bounding box
# 
#    <score>	     The score in the DETECTION file indicates the confidence of the predicted bounding box enclosing 
#                      an object instance.
#                      The score in GROUNDTRUTH file is set to 1 or 0. 1 indicates the bounding box is considered in evaluation, 
#                      while 0 indicates the bounding box will be ignored.
#                       
# <object_category>    The object category indicates the type of annotated object, (i.e., ignored regions(0), pedestrian(1), 
#                      people(2), bicycle(3), car(4), van(5), truck(6), tricycle(7), awning-tricycle(8), bus(9), motor(10), 
#                      others(11))
#                       
# <truncation>	     The score in the DETECTION result file should be set to the constant -1.
#                      The score in the GROUNDTRUTH file indicates the degree of object parts appears outside a frame 
#                      (i.e., no truncation = 0 (truncation ratio 0%), and partial truncation = 1 (truncation ratio 1% ~ 50%)).
#                       
# <occlusion>	     The score in the DETECTION file should be set to the constant -1.
#                      The score in the GROUNDTRUTH file indicates the fraction of objects being occluded (i.e., no occlusion = 0 
#                      (occlusion ratio 0%), partial occlusion = 1 (occlusion ratio 1% ~ 50%), and heavy occlusion = 2 
#                      (occlusion ratio 50% ~ 100%)).
# 
# ```

import json
from pathlib import Path
from PIL import Image
import pandas as pd
from tqdm import tqdm


def parse_image(image_id: int,
                image_path: Path) -> dict: 
    """ 
        Read the image and parse the image information int json format
                Args:
        """
    img = Image.open(image_path)  
    width, height = img.size

    image= {
            "file_name": str(image_path.name),
            "height": height,
            "width": width,
            "id": int(image_id)
    }

    return image

def parse_annotations(image_id: int,
                      file_path: Path,
                      ) -> list[dict]:
        """
        Read and parse annotations
        Args:
                image_id: the id of the image
                file_path: the path to the annotation file
        Returns:
                annotations: the list of annotations in coco format
        """
        annotations = []
        columns = ['bbox_left', 
                   'bbox_top', 
                   'bbox_width', 
                   'bbox_height', 
                   'score', 
                   'object_category', 
                   'truncation', 
                   'occlusion']
        df = pd.read_csv(file_path, sep=',', header=None)

        if df.shape[1] == len(columns):
                df.columns = columns
        else:
               print("[ERROR] bad columns")
               print(file_path)
               print(df.shape)
               raise ValueError("badcolumns")
        
        
        for _, row in df.iterrows():
                ann ={}
                ann["image_id"] = image_id
                ann["segmentation"] = []
                ann["bbox"] = [row['bbox_left'],
                        row['bbox_top'],
                        row['bbox_width'],
                        row['bbox_height']]
                ann["category_id"] = row['object_category']
                ann["area"]=row['bbox_width'] * row['bbox_height']
                ann["iscrowd"] = 0
                ann["score"] = row['score']
                ann["oclusion"] = row['occlusion']
                ann["truncation"] = row['truncation']
                
                annotations.append(ann)
        
        return annotations
                        
def get_image_and_annotations(file_id: int ,
                                images_dir: str = "images",
                                file_path : str = None)-> [dict , list]:
    """
        Get the image and annotations from the annotation file
        Args:
                file_id: the id of the file which is the same as the image id
                images_dir: the directory of the images
                file_path: the path to the annotation file
        Returns:
                image: dict with the image information
                annotations: the list of annotations in coco format

            """

    file_path = Path(str(file_path))
    dataset_root_dir=file_path.parent.parent

    file_name = file_path.stem
    image_name = file_name + ".jpg"
    image_path = dataset_root_dir /images_dir/ image_name
    
    assert (file_path.suffix == ".txt" 
            and image_path.suffix =='.jpg'
            and image_path.exists() ), "File path is not valid"
    
    # Read and parse image to image dict
    image = parse_image(image_id=file_id,
                        image_path=image_path)

    # Read and parse annotations to annotations list of dicts
    try:
        annotations=parse_annotations(image_id=file_id,
                                    file_path=file_path)
        return image, annotations
    except Exception as e:
           raise ValueError("Error parsing annotations")
    
def convert_visdrone_to_coco(info : dict = None,
                            visdrone_path : str = "data/visdrone/",
                            annotations_dir : str = "annotations",
                            class_names:list=None) -> dict:
    
    """
        Convert visdrone dataset annotations from txt to coco format
    """


    # ##
    # create a dictionary for the coco format

    visdrone_coco_format = {
        "info": {
            "description": "VisDrone Dataset",
            "url": "https://github.com/VisDrone/VisDrone-Dataset",
            "version": "1.0",
            "year": 2019,
            "contributor": "VisDrone",
            "date_created": "Aug 25, 2019"
        } if not info else info,
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # ##
    ## Categories from  https://github.com/VisDrone/VisDrone2018-DET-toolkit
    class_names = ['ignored regions', 
                        'pedestrian',
                        'people',
                        'bicycle',
                        'car',
                        'van',
                        'truck',
                        'tricycle',
                        'awning-tricycle',
                        'bus',
                        'motor',
                        'others'] if not class_names else class_names

    categories= [{"id": i, "name": cat} for i,cat in enumerate(class_names)]

    # ##
    # add categories to the dictionary
    visdrone_coco_format["categories"].extend(categories)

    # ## [markdown]
    # **Extract the annotations**

    # Path to the images and annotations
    visdrone_path = Path(str(visdrone_path))
    annotations_path = visdrone_path/ annotations_dir
    all_annotation_files = list(annotations_path.glob("*.txt"))

    # we will iterate for each file and extract annotations
    for file_id, file_path in enumerate(tqdm(all_annotation_files),1):
        try:
            image, annotations = get_image_and_annotations(file_id=file_id,                                                   
                                                    file_path=file_path)
            
            visdrone_coco_format["images"].append(image)
            visdrone_coco_format["annotations"].extend(annotations)

        except Exception as e:
            print("[ERROR] error parsing annotations")
            print(file_path)
            print("_"*50)
            continue

    # ##
    # generate ids for annotations
    for i, ann in enumerate(visdrone_coco_format["annotations"], 1):
        ann["id"] = i

    return visdrone_coco_format







