import sys
import codecs
import numpy as np
import shapely.geometry as shgeo
import os
import re
import math
import cv2
import json
from PIL import Image
from pathlib import Path
from  tqdm.auto import tqdm

# import polyiou
"""
	some basic functions which are useful for process uav123 dataset
"""


def convert_uav123_to_coco(DATA_PATH : str = 'data/uav123/',
						  annotations_dir : str = 'annotations',
						  annotation_file : str = 'uav123.json',):
  
	"""
	convert the uav123 dataset to coco format
	"""
	annotation_file = Path(DATA_PATH)/annotations_dir/annotation_file
	dataset = json.load(open(annotation_file, 'r'))
	assert type(dataset)==dict, 'annotation file format {} not supported'.format(type(dataset))

	ret = {
		"info": {
			"description": "UAV123  Dataset",
			"url": "https://cemse.kaust.edu.sa/ivul/uav123",
			"version": "v1.0",
			"year": 2016,
			"contributor": "IVUL",
			"date_created": " 2016"}
	}

	ret.update(dataset)

		

	print("# images: ", len(ret['images']))
	print("# annotations: ", len(ret['annotations']))

	return ret


