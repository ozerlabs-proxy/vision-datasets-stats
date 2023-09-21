# Dataset Statistics

In `computer vision`, we have a lot of datasets that are used for different tasks. These datasets are used to train and test models. The datasets are usually in the form of images, videos, or both. The datasets are usually annotated with labels that are used to train the models. The labels are usually in the form of bounding boxes, segmentation masks, or both.

For the 3 main tasks in computer vision (`Detection`, `Segmentation`, and `Tracking`), we are going to look at the datasets that are used for each task. We are going to look at the statistics of each dataset and perform a comparison in the end.

To do this we will need to load each dataset and extract it's statistics programatically. We will also need to visualize the statistics in a way that is easy to understand. We will also need to compare the statistics of each dataset and see how they compare to each other.


The task flow will be as follows:

For each task;
* research task specific datasets. 
For each dataset;
    - [ ] 1. Download the dataset
    - [ ] 2. Write dataset loaders
    - [ ] 3. Extract the statistics
    - [ ] 4. Save the statistics
    - [ ] 5. Visualize the statistics
    - [ ] 6. Compare the statistics
    - [ ] 7. Write a report



## Datasets

### Detection Datasets

1. `COCO`
    Introduced by Tsung-Yi Lin et al. in Microsoft COCO: Common Objects in Context. [read more](https://cocodataset.org/#home)

2. `SkyData` 
    Our dataset: SkyData: UAV taken images dataset for object detection and tracking.

3. `VisDrone DET` Vision Meets Drones: collected by the AISKYEYE team at Lab of Machine Learning and Data Mining, Tianjin University, China. The dataset consists of `288 video` clips formed by `261,908 frames` and `10,209 static` images, captured by various drone-mounted cameras.  [read more](https://github.com/VisDrone/VisDrone-Dataset)

4. `KAIST` a Multispectral(RGB-Thermal) Pedestrian Detection Challenge. The KAIST Multispectral Pedestrian Dataset is imaging hardware consisting of a color camera, a thermal camera and a beam splitter to capture the aligned multispectral `(RGB color + Thermal)` images. With this hardware, we captured various regular traffic scenes at day and night time to consider changes in light conditions. and, consists of 95k color-thermal pairs `(640x480, 20Hz)` taken from a `vehicle`. All the pairs are manually annotated (`person`, `people`, `cyclist`) for the total of `103,128` dense annotations and `1,182` unique pedestrians.  [read more](https://eval.ai/web/challenges/challenge-page/1247/evaluation)

6. `VHR-10` Very High Resolution Vehicle Detection in Aerial Imagery. The VHR-10 is a  10-class geospatial object detection dataset. These ten classes of objects are `airplane`, `ship`, `storage tank`, `baseballdiamond`, `tennis court`, `basketball court`, `ground track field`, `harbor`, `bridge`, and `vehicle`. This dataset contains totally `800 very-high-resolution (VHR)` remote sensing images that were cropped from `Google Earth` and `Vaihingen dataset` and then `manually annotated` by experts. [read more](https://gcheng-nwpu.github.io/)






## Detection datasets 

* [x] 1. COCO
* [x] 2. SkyData
* [x] 3. VisDrone DET
* [x] 4. ~~KAIST (not sure it is original)~~
* [x] 5. KAIST (larger version)
* [ ] 6. VHR-10 
* [ ] 6. KITTI
* [ ] 7. MOTS
* [ ] 9. DOTA
* [ ] 10. VEDAI dataset

## Segmentation datasets
### Semantic Segmentation Datasets
* [ ] 1. COCO
* [ ] 2. SkyData
* [ ] 3. KITTI
* [ ] 4. VHR-10

### Instance Segmentation
* [ ] 1. COCO
* [ ] 2. SkyData

## Tracking Datasets
### Single Object Tracking Datasets
* [ ] 1. SkyData
* [ ] 2. VisDrone-SOT
* [ ] 3. UAV123

### Multiobject Tracking Datasets [MOT]

* [ ] 1. VisDrone-MOT 
* [ ] 2. MOTS
* [ ] 3. SkyData
* [ ] 4. KAIST
* [ ] 5. UAV123

## Video Instance Segmentation Datasets
* [ ] 1. Youtube-VIS
* [ ] 2. SkyData



# Note to self 

- [ ] 1. Create a list of datasets to be used for each task
- [ ] 2. Create a list of models to be used for each task
- [ ] 3. get necessary statistics from the above datasets
