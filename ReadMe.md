# Dataset Statistics

In `computer vision`, we have a lot of datasets that are used for different tasks. These datasets are used to train and test models. The datasets are usually in the form of images, videos, or both. The datasets are usually annotated with labels that are used to train the models. The labels are usually in the form of bounding boxes, segmentation masks, or both.

For the 3 main tasks in computer vision (`Detection`, `Segmentation`, and `Tracking`), we are going to look at the datasets that are used for each task. We are going to look at the statistics of each dataset and perform a comparison in the end.

To do this we will need to load each dataset and extract it's statistics programatically. We will also need to visualize the statistics in a way that is easy to understand. We will also need to compare the statistics of each dataset and see how they compare to each other.


<!-- The task flow will be as follows:

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
 -->

<!-- 
## Datasets

### Detection Datasets

1. `COCO`
    Introduced by Tsung-Yi Lin et al. in Microsoft COCO: Common Objects in Context. [read more](https://cocodataset.org/#home)

2. `SkyData` 
    Our dataset: SkyData: UAV taken images dataset for object detection and tracking.

3. `VisDrone DET` Vision Meets Drones: collected by the AISKYEYE team at Lab of Machine Learning and Data Mining, Tianjin University, China. The dataset consists of `288 video` clips formed by `261,908 frames` and `10,209 static` images, captured by various drone-mounted cameras.  [read more](https://github.com/VisDrone/VisDrone-Dataset)

4. `KAIST` a Multispectral(RGB-Thermal) Pedestrian Detection Challenge. The KAIST Multispectral Pedestrian Dataset is imaging hardware consisting of a color camera, a thermal camera and a beam splitter to capture the aligned multispectral `(RGB color + Thermal)` images. With this hardware, we captured various regular traffic scenes at day and night time to consider changes in light conditions. and, consists of 95k color-thermal pairs `(640x480, 20Hz)` taken from a `vehicle`. All the pairs are manually annotated (`person`, `people`, `cyclist`) for the total of `103,128` dense annotations and `1,182` unique pedestrians.  [read more](https://eval.ai/web/challenges/challenge-page/1247/evaluation)

6. `VHR-10` Very High Resolution Vehicle Detection in Aerial Imagery. The VHR-10 is a  10-class geospatial object detection dataset. These ten classes of objects are `airplane`, `ship`, `storage tank`, `baseballdiamond`, `tennis court`, `basketball court`, `ground track field`, `harbor`, `bridge`, and `vehicle`. This dataset contains totally `800 very-high-resolution (VHR)` remote sensing images that were cropped from `Google Earth` and `Vaihingen dataset` and then `manually annotated` by experts. [read more](https://gcheng-nwpu.github.io/)


7. `DOTA` [A Large-Scale Benchmark and Challenges for Object Detection in Aerial Images](https://captain-whu.github.io/DOTA/index.html). `DOTA` is a large-scale dataset for object detection in aerial images. The DOTA images are collected from the Google Earth, GF-2 and JL-1 satellite provided by the China Centre for Resources Satellite Data and Application, and aerial images provided by CycloMedia B.V. DOTA consists of RGB images and grayscale images. The RGB images are from Google Earth and CycloMedia, while the grayscale images are from the panchromatic band of GF-2 and JL-1 satellite images. All the images are stored in 'png' formats.

    It can be used to develop and evaluate object detectors in aerial images. The images are collected from different sensors and platforms. Each image is of the size in the range from `800 × 800` to `20,000 × 20,000 pixels` and contains objects exhibiting a wide variety of scales, orientations, and shapes. The instances in DOTA images are `annotated by experts in aerial image` interpretation by arbitrary (8 d.o.f.) quadrilateral. Currently DOTA has 3 versions: 

    - `DOTA-v1.0` contains 15 common categories, `2,806 images` and 1`88, 282 instances.`
    - `DOTA-v1.5`  same images as `DOTA-v1.0`, but the extremely small instances (less than 10 pixels) are also annotated. Moreover, a new category, ”container crane” is added. 
    - `DOTA-v2.0` latest and contains more categories, images and instances. collects more Google Earth, GF-2 Satellite, and aerial images. There are 18 common categories, `11,268 images` and `1,793,658 instances` in `DOTA-v2.0.` Compared to `DOTA-v1.5`, it further adds the new categories of ”airport” and ”helipad”.

We will explore the `DOTA-v2.0` dataset. [read more...](https://captain-whu.github.io/DOTA/index.html)

8. `VEDAI` (Vehicle Detection in Aerial Imagery) : a dataset for Vehicle Detection in Aerial Imagery, provided as a tool to benchmark automatic target recognition algorithms in unconstrained environments. The vehicles contained in the database, in addition of being small, exhibit different variabilities such as multiple orientations, lighting/shadowing changes, specularities or occlusions. Furthermore, each image is available in several spectral bands and resolutions. [read more](https://downloads.greyc.fr/vedai/)

9. `KITTI` (Karlsruhe Institute of Technology and Toyota Technological Institute) : a large-scale dataset for object detection, object tracking, and more. The dataset consists of `grayscale` and `color` images, as well as `velodyne` point clouds and `calibration` data. This raw data is annotated with object bounding boxes and instance segmentations. [read more](http://www.cvlibs.net/datasets/kitti/)

10. `UAV123` (UAV123@CVPR2018) : a benchmark dataset for UAV-based object tracking. It consists of 123 video sequences captured by various UAVs in different scenarios. The dataset is divided into three subsets, i.e., UAV20L, UAV123_10fps and UAV123_30fps, according to the frame rate of the videos. [read more](https://ivul.kaust.edu.sa/Pages/pub-benchmark-simulator-uav.aspx)


 -->

## Task based datasets lookup table

<table style="list-style: none;">
    <thead>
        <tr>
            <th>Task</th>
            <th>Detection</th>
            <!-- <th>Semantic Segmentation</th> -->
            <th>Instance Segmentation</th>
            <!-- <th>Single Object Tracking</th> -->
            <th>Multi Object Tracking</th>
            <th>Video Instance Segmentation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Dataset</th>
            <td><!-- det -->
                <li>✓ COCO</li>
                <li>✓ SkyData </li>
                <li>✓ VisDrone</li>
                <li>✓ KAIST </li>
                <li>✓ VHR-10 </li>
                <li>✓ DOTA </li>
                <li>✓ VEDAI </li>
                <li>✓ KITTI </li>
            </td>
            <!-- <td>
                <li> COCO</li>
                <li> SkyData </li>
                <li> KITTI </li>
                <li> VHR-10 </li>
                <li> MOTS </li>
            </td> -->
            <td><!-- seg -->
                <li>✓ COCO</li>
                <li>✓ SkyData </li>
                <li>✓ VHR-10 </li>
            </td>
            <!-- <td>
                <li>SkyData</li>               
                <li> UAV123 </li>               
                <li> VOT2018 </li>              
            </td> -->
            <td><!-- mot -->
                <li>✓ SkyData</li>
                <li>✓ VisDrone-MOT </li>
                <li>✓ MOT-CHALLENGE </li>
                <li> KAIST </li>
                <!-- <li> Lvis </li>
                <li> TAO </li> -->
            </td>
            <td><!-- vis -->
                <li>✓ SkyData</li>
                <li>✓ Youtube-VIS 2019 </li>
                <li>✓ Youtube-VIS 2021 </li>
            </td>
        </tr>
    </tbody>
</table>


# Stats 

There is a number of stats about datasets that can be generated. These may vary depending on the task, for most we will derive the following:
<table>
    <thead>
        <tr>
            <th> - </th>
            <th>Detection</th>
            <th>Tracking</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Stats</th>
            <td>
                <ol>
                    <li>✓ Number of images</li>
                    <li>✓ Number of objects</li>
                    <li>✓ Number of classes</li>
                    <li>✓ Number of instances per class</li>
                    <li>✓ Average number of instances per image</li>
                    <li>✓ Average number of instances per class</li>
                </ol>
            </td>
            <td>
                <ol>
                    <li>✓ Number of videos</li>
                    <li>✓ Number of tracks</li>
                    <li>✓ Number of categories</li>
                    <li>✓ average track length</li>
                    <li>✓ average number of tracks per video</li>
                    <li>✓ average number of tracks per category</li>
                    <li>✓ video lengths</li>
                    <li>✓ min-max resolutions</li>
                    <li>✓ areas stats ... </li>
                </ol>
            </td>
        </tr>
    </tbody>
</table>

# Note to self 
