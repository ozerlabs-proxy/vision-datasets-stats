"""
contains tools to vedai annotations to coco format.
"""
import json
from pathlib import Path
from PIL import Image
import pandas as pd
from tqdm.auto import tqdm


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
    
def convert_vedai_to_coco(info : dict = None,
                            visdrone_path : str = "data/vedai/",
                            annotations_dir : str = "annotations",
                            class_names:list=None) -> dict:
    
    """
        Convert vedai dataset to coco format
    """


    # ##
    # create a dictionary for the coco format

    visdrone_coco_format = {
        "info": {
            "description": "VEDAI Dataset",
            "url": "https://downloads.greyc.fr/vedai/",
            "version": "1.0",
            "year": 2015,
            "contributor": "VEDAI",
            "date_created": "2015"
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







