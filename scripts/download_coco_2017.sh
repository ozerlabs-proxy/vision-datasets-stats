#!/bin/bash

mkdir -p "data/coco/2017"
cd "data/coco/2017"

wget -c http://images.cocodataset.org/annotations/annotations_trainval2017.zip
wget -c http://images.cocodataset.org/annotations/image_info_test2017.zip
# wget -c http://images.cocodataset.org/annotations/stuff_annotations_trainval2017.zips
# wget -c http://images.cocodataset.org/annotations/image_info_unlabeled2017.zip

unzip annotations_trainval2017.zip 
unzip image_info_test2017.zip
# unzip stuff_annotations_trainval2017.zip
# unzip image_info_unlabeled2017.zip

rm annotations_trainval2017.zip
rm image_info_test2017.zip
# rm stuff_annotations_trainval2017.zip
# rm image_info_unlabeled2017.zip