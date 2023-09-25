#!/bin/bash

current_dir=$(pwd)

# rm -rf
rm -rf "$HOME/shortcuts/Datasets/vedai/"

mkdir -p "$HOME/shortcuts/Datasets/vedai/"
cd "$HOME/shortcuts/Datasets/vedai/"

wget -c https://downloads.greyc.fr/vedai/Annotations512.tar 
wget -c https://downloads.greyc.fr/vedai/Annotations1024.tar
# wget -c https://downloads.greyc.fr/vedai/DevKit.tar

tar -xvf Annotations512.tar
tar -xvf Annotations1024.tar
# tar -xvf DevKit.tar


# It is easier to work with single file that has it all instead of multiple files
mkdir -p "$HOME/shortcuts/Datasets/vedai/annotations"
cp Annotations512/annotation512.txt annotations
cp Annotations1024/annotation1024.txt annotations




# # Move all annotations to a single folder 
mkdir -p "$HOME/shortcuts/Datasets/vedai/all_annotations"
mv Annotations512 all_annotations/
mv Annotations1024 all_annotations/

# remove the tar files
rm Annotations512.tar
rm Annotations1024.tar
# rm DevKit.tar


# # create links to the dataset folder 

# # make veda in current dir and create links to the dataset folder
mkdir -p "$current_dir/data/vedai"
ln -s "$HOME/shortcuts/Datasets/vedai/annotations" "$current_dir/data/vedai/"
