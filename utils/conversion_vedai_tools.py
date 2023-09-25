"""
contains tools to vedai annotations to coco format.
"""
import json
from pathlib import Path
from PIL import Image
import pandas as pd
import numpy as np
import shapely.geometry as shgeo

from tqdm.auto import tqdm

IMG_SIZE_512 = 512
IMG_SIZE_1024 = 1024

def parse_image(image_id: int,
                image_path: Path,
                img_size: list = [IMG_SIZE_512,IMG_SIZE_512]) -> dict: 
    """ 
        Read the image and parse the image information int json format
                Args: 
        """
    # the size is already know no need to read the image
    img = None
        #img = Image.open(image_path)  
    width, height = img_size

    image= {
            "file_name": str(image_path.name),
            "height": height,
            "width": width,
            "id": int(image_id)
    }

    return image

def parse_annotation(row: None) -> list[dict]:
        """
        Read and parse annotations
        Args:
                image_id: the id of the image
                file_path: the path to the annotation file
        Returns:
                annotations: the list of annotations in coco format
        """

        box_info = {}
        box_info['poly'] = [(float(row['x1']), float(row['y1'])),
                                (float(row['x2']), float(row['y2'])),
                                (float(row['x3']), float(row['y3'])),
                                (float(row['x4']), float(row['y4']))
                                ]

        bbx_raw = list(map(int, np.array( box_info['poly']).flatten()))        
        gtpoly = shgeo.Polygon(box_info['poly'])
        box_info['area'] = gtpoly.area



        xmin, ymin, xmax, ymax = min(bbx_raw[0::2]), min(bbx_raw[1::2]), \
                                        max(bbx_raw[0::2]), max(bbx_raw[1::2])

        width, height = xmax - xmin, ymax - ymin
        
        ann ={}
        ann["image_id"] = int(row['image_id'])
        ann["center_x"] = row['center_x']
        ann["center_y"] = row['center_y']
        ann["orientation"] = row['orientation']
        ann["category_id"] = row['class_id']
        ann["iscrowd"] = 0
        ann["score"] = 1
        ann["oclusion"] = row['is_occluded']
        ann["truncation"] = row['is_contained']

        ann["segmentation"] = []
        ann["bbox"] = [xmin, ymin, width, height]
        # ann["area"]=height*width

        return ann
   
def convert_vedai_to_coco(info : dict = None,
                            dataset_path : str = "data/vedai/",
                            annotations_dir : str = "annotations",
                            annotations_file: str = "annotation512.txt",
                            class_names: dict = None) -> dict:
    
    """
        Convert vedai dataset to coco format
    """



    # ##
    # create a dictionary for the coco format

    _coco_format = {
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
    ## Categories #TODO they need to be revisted and updated.
    class_names = {1 : "car",
                        2 : "truck",
                        3 : "pickup",
                        4 : "tractor",
                        5 : "camping",
                        6 : "boat",
                        7 : "motorcycle",
                        8 : "category 8",
                        9 : "bus",
                        10 : "van",
                        11 : "others",
                        12 : "small vehicle",
                        13 : "large vehicl", 
                        31 : "plane",
                        23 : "board"} if not class_names else class_names

    categories= [{"id": i, "name": cat , "supercategory": None} for i,cat in class_names.items()]

    # ##
    # add categories to the dictionary
    _coco_format["categories"].extend(categories)

    # ## [markdown]
    # **Extract the annotations**

    # Path to the images and annotations
    dataset_path = Path(str(dataset_path))
    annotations_path = dataset_path/ annotations_dir
    annotation_file = annotations_path/ annotations_file

    assert (annotation_file.exists() 
            and annotation_file.suffix == ".txt"), f"{annotation_file} File path is not valid"
    

    # read the annotaions file and parse each line
    df = pd.read_csv(annotation_file, sep=" ", header=None, index_col=False)
    assert df.shape[1] == 15, "bad columns"
    columns=['image_id','center_x','center_y','orientation','x1','y1','x2', 'y2','x3','y3','x4','y4', 'class_id','is_contained','is_occluded']

    df.columns = columns
    df['image_id'] = df['image_id'].astype(int)
    
    seen_image_ids=[]

    for i, row in tqdm(df.iterrows(), total=df.shape[0]):

        image_id = int(row['image_id'])

        if image_id not in seen_image_ids:
            seen_image_ids.append(image_id)

            image_path = dataset_path / "images" / f"{image_id}.jpg"
            image = parse_image(image_id=image_id,
                                image_path=image_path)
            _coco_format["images"].append(image)

        annotation = parse_annotation(row=row)
        
        _coco_format["annotations"].append(annotation)

 
    # ##
    # generate ids for annotations
    for i, ann in enumerate(_coco_format["annotations"], 1):
        ann["id"] = i

    return _coco_format







