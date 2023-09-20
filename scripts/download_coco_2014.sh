#!/bin/bash

mkdir -p "data/coco/2014"
cd "data/coco/2014"

wget -c  http://images.cocodataset.org/annotations/annotations_trainval2014.zip
wget -c  http://images.cocodataset.org/annotations/image_info_test2014.zip


unzip annotations_trainval2014.zip 
unzip image_info_test2014.zip

rm annotations_trainval2014.zip
rm image_info_test2014.zip
