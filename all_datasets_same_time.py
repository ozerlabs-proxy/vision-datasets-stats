# # %% [markdown]
# # # Datasets
# # 
# # All dataset will have classes that read annotations. The dataset class needs to extend our custom `BaseDataset` class. 
# # 
# # The `BaseDataset` class has the following methods:
# # 
# # * `generate_dataset_statistics`: generates a summary of the dataset (e.g. number of images, number of annotations, etc.)
# # * `save_dataset_statistics`: saves the summary to a `json` file
# # 
# # 
# # 

# # %% [markdown]
# # ## **0. Toy example**
# # - get dataset instance
# # - create index
# # - generate statistics
# # - save statistics
# # 

# # %% [markdown]
# # 

# # %% [markdown]
# # ``` python
# # 
# # # 0. Toy example
# # 
# # from bases.example import Example
# # 
# # D = Example()
# # 
# # # generate and load stats
# # D.generate_dataset_statistics()
# # 
# # # save the stats
# # D.save_dataset_statistics(save_path = "./summaries",
# #                             dataset_name = None,
# #                             file_name = None
# #                             )
# # 
# # ```

# # %% [markdown]
# # ## **1. COCO 2017 dataset**
# # 
# # ``` python
# # ## 1. COCO dataset
# # 
# from bases.coco import COCO
# from pathlib import Path

# coco_year = 2017
# subset = f"instances_train{coco_year}"
# annotiation_file = Path(f"./data/coco/{coco_year}/annotations/{subset}.json")
# D = COCO(annotation_file=str(annotiation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"coco{coco_year}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print("*"*50)
# # ```

# # %% [markdown]
# # ## **1. COCO 2014 dataset**
# # 
# # ``` python
# # ## 1. COCO dataset
# # 
# from bases.coco import COCO
# from pathlib import Path

# coco_year = 2014
# subset = f"instances_train{coco_year}"
# annotiation_file = Path(f"./data/coco/{coco_year}/annotations/{subset}.json")
# D = COCO(annotation_file=str(annotiation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"coco{coco_year}",
#                             file_name = f"{subset}_stats.json"
#                             )
# print("*"*50)
# # ```

# # %% [markdown]
# # ## **2. SkyData dataset**
# # 
# # 
# # ```python
# # ## 2. Skydata 
# 
# from bases.skydata import SkyData
# from pathlib import Path

# subset = f"train_DET"
# annotiation_file = Path(f"./data/skydata/annotations/{subset}.json")
# D = SkyData(annotation_file=str(annotiation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"skydata",
#                             file_name = f"{subset}_stats.json"
#                             )

# print("*"*50)
# # ```

# # %% [markdown]
# # 
# # ## **3. Visdrone dataset**
# # 
# # 
# # ```python
# # ## 3. Visdrone 
# # 
# from bases.visdrone import VisDrone
# from pathlib import Path

# import os


# converted_path = Path("./data/visdrone/converted_annotations")
# annotation_file = converted_path / "visdrone_converted_to_coco_format.json"

# # if annotation_file does not exist, convert the dataset
# if not annotation_file.exists():

#     try:
#         #TODO this could be improved 
#         # The script could take arguments 
#         print("[INFO] Converting visdrone dataset to COCO format...")
#         os.system("python ./scripts/convert_visdrone_to_coco_format.py")
#         print("[INFO] Finished converting dataset to COCO format.")
#     except:
#         print("[ERROR] Could not convert dataset to COCO format.")
#         exit(1)


# D = VisDrone(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"visdrone",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )
# print("*"*50)                            
# # ```

# # %% [markdown]
# # ## **4. KAIST ROBOFLOW dataset**
# # 
# # ```python
# # ## 4. KAIST_roboflow 
# # 
# from bases.kaist import KAIST
# from pathlib import Path

# import os


# converted_path = Path("./data/kaist_roboflow/annotations")
# annotation_file = converted_path / "kaist_train_annotations_coco.json"

# D = KAIST(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"kaist_roboflow",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )
# print("*"*50)
# # ```

# # %% [markdown]
# # ## **5. KAIST pedestrian dataset**
# # 
# # ```python
# # 
# # ## 5. KAIST pedestrian dataset
# # 
# from bases.kaist_pedestrian import KAIST
# from pathlib import Path

# import os


# converted_path = Path("./data/kaist_pedestrian/converted_annotations")
# annotation_file = converted_path / "kaist_converted_to_coco_format.json"

# D = KAIST(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"kaist_pedestrian",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )

# print("*"*50)
# # ```

# # %% [markdown]
# # ## **6. VHR10**
# # 
# # ```python
# # ## 6. VHR10
# # 
# from bases.vhr import VHR10
# from pathlib import Path

# import os


# converted_path = Path("./data/vhr_10/annotations")
# annotation_file = converted_path / "vhr_annotations.json"

# D = VHR10(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"vhr_10",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )

# print("*"*50)
# # 
# # ```

# # %% [markdown]
# # 
# # ## **7. DOTA v2.0 dataset**
# # 
# # 
# # ```python
# # ## 7. DOTA train dataset 
# # 
# from bases.dota import DOTA
# from pathlib import Path

# import os


# converted_path = Path("./data/dota/converted_annotations")
# annotation_file = converted_path / "dotav2_converted_to_coco.json"

# # if annotation_file does not exist, convert the dataset
# if not annotation_file.exists():

#     try:
#         #TODO this could be improved 
#         # The script could take arguments 
#         print("[INFO] Converting dota dataset to COCO format...")
#         os.system("python ./scripts/convert_dota_to_coco_format.py")
#         print("[INFO] Finished converting dataset to COCO format.")
#     except:
#         print("[ERROR] Could not convert dataset to COCO format.")
#         exit(1)


# D = DOTA(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"DOTA",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )
                            
# print("*"*50)                           
# # ```

# # %% [markdown]
# # 
# # 
# # ## **8. VEDAI dataset**
# # 
# # 
# # ```python
# # ## 8. Vedai dataset 
# # 
# from bases.vedai import VEDAI
# from pathlib import Path

# import os


# converted_path = Path("./data/vedai/converted_annotations")
# annotation_file = converted_path / "vedai_converted_to_coco_format.json"

# # if annotation_file does not exist, convert the dataset
# if not annotation_file.exists():

#     try:
#         #TODO this could be improved 
#         # The script could take arguments 
#         print("[INFO] Converting vedai dataset to COCO format...")
#         os.system("python ./scripts/convert_vedai_to_coco_format.py")
#         print("[INFO] Finished converting dataset to COCO format.")
#     except:
#         print("[ERROR] Could not convert dataset to COCO format.")
#         exit(1)


# D = VEDAI(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"vedai",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )

# print("*"*50)                     
# # ```

# # %% [markdown]
# # 
# #                           
# # 
# # ## **9. KITTI dataset**
# # 
# # 
# # ```python
# # ## 9. KITTI dataset
# # 
# from bases.kittidet import KITTI
# from pathlib import Path

# import os


# converted_path = Path("./data/kitti/converted_annotations")
# annotation_file = converted_path / "kitti_converted_to_coco_format.json"

# # if annotation_file does not exist, convert the dataset
# if not annotation_file.exists():

#     try:
#         #TODO this could be improved 
#         # The script could take arguments 
#         print("[INFO] Converting kitti dataset to COCO format...")
#         os.system("python ./scripts/convert_kitti_to_coco.py")
#         print("[INFO] Finished converting dataset to COCO format.")
#     except:
#         print("[ERROR] Could not convert dataset to COCO format.")
#         exit(1)


# D = KITTI(annotation_file=str(annotation_file))

# # generate and load stats
# D.generate_dataset_statistics()

# # save the stats
# D.save_dataset_statistics(save_path = "./summaries",
#                             dataset_name = f"kitti",
#                             file_name = f"{annotation_file.stem}_stats.json"
#                             )

# print("*"*50)
                            
# # ```  


