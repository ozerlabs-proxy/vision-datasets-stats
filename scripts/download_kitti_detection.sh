#!/bin/bash

current_dir=$(pwd)

# rm -rf
rm -rf "$HOME/shortcuts/Datasets/kitti/"

mkdir -p "$HOME/shortcuts/Datasets/kitti/"
cd "$HOME/shortcuts/Datasets/kitti/"

wget -c https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip
wget -c https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip

unzip data_object_image_2.zip
unzip data_object_label_2.zip




# remove the tar files
rm data_object_image_2.zip
rm data_object_label_2.zip

# # make veda in current dir and create links to the dataset folder
mkdir -p "$current_dir/data/kitti"
ln -s "$HOME/shortcuts/Datasets/kitti/image_2" "$current_dir/data/kitti/"
ln -s "$HOME/shortcuts/Datasets/kitti/label_2" "$current_dir/data/kitti/"