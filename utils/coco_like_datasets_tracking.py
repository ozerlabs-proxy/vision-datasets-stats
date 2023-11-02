
from bases.base_dataset_functionality import BaseDatasetTracking
from collections import defaultdict
import numpy as np


def generate_stats_coco_like(D:BaseDatasetTracking) -> dict:

    """
        TODO: Generate statistics for coco like datasets.
        D contains information needed to generate summaries for videos
        
        stats to generate:
        videos_stats:
                    - videos_count
                    
        categories_stats

    """

    stats = defaultdict(dict)

    #info 
    stats["info"] =  {} if "info" not in D.dataset else D.dataset["info"] 
    
    #images stats
    stats["_general_stats"] = get_general_videos_stats(list(D.videos.values()))

    # #category stats 
    stats["_cats"] = categories_and_super_categories_stats(list(D.cats.values()))
    
    stats["_categories_stats"] = get_categories_stats(list(D.cats.values()),
                                                        D.catsToTracks, 
                                                        D.catToVids)
    
    #check if instance of  a class has a given attribute(variable) in python 
    
    
    useAnns = None
    try:
        useAnns = D.adjustedAnns 
        if useAnns is None:
            raise Exception("Anns should not be None")
    except:
        useAnns = D.anns
    
    assert useAnns is not None, "Anns should not be None"
  # general areas stats
    stats["_areas_stats"] = get_areas_stats(useAnns)

    #tracks stats
    stats["tracks_stats"] = get_tracks_stats( D.tracksToFrames,
                                                D.vidToTracks)
    return stats

def  get_tracks_stats(tracksToFrames,
                      vidToTracks
                      ):
    
    _stats={ 
            "total_tracks": len(tracksToFrames),
            "average_track_length": 0,
            "min_track_length": 0,
            "max_track_length": 0,
            "average_tracks_per_video": 0,
            }
    
    _stats["average_track_length"] = np.mean([len(v) for v in tracksToFrames.values()])
    _stats["min_track_length"] = np.min([len(v) for v in tracksToFrames.values()])
    _stats["max_track_length"] = np.max([len(v) for v in tracksToFrames.values()])
    _stats["average_tracks_per_video"] = np.mean([len(v) for v in vidToTracks.values()])

    return _stats


def get_categories_stats(cats,
                        catsToTracks, 
                        catToVids):
    
    _stats = {
        
        "category_names": [],
        "per_cat_tracks": [],
        "cat_in_n_vids": []
        
    }
    _stats["category_names"] = [cat["name"] for cat in cats]
    _stats["per_cat_tracks"] = [len(catsToTracks[cat["id"]]) for cat in cats]
    _stats["cat_in_n_vids"] = [len(catToVids[cat["id"]]) for cat in cats]
    
    return _stats
    

def categories_and_super_categories_stats(categories):
    
    _stats = {
        "categories_count": 0,
        "super_categories_count": 0,
        "categories": {},
        "super_categories": {}
        
    }
    
    _stats["categories_count"] = len(categories)
    _stats["categories"] = {cat["id"]: cat["name"] for cat in categories}
    _stats["super_categories"] ={}
    if "supercategory" in categories[0]:
        _stats["super_categories"] = { i:v for i,v in enumerate(list(set([cat["supercategory"] for cat in categories])))} 
    _stats["super_categories_count"] = len(_stats["super_categories"])
    
    return _stats
    
    

def get_general_videos_stats(videos : list[dict] = []):  
    """
    Given a list of videos, return the number of videos, the minimum and maximum resolution.

    """     
    _stats = {
        "videos_count": 0,
        }
    if type(videos) == list and len(videos) == 0:
        return _stats
    
    
    _stats["videos_count"] = len(videos)
    _stats["min_resolution"] = min([video["height"]*video["width"] for video in videos])
    _stats["max_resolution"] = max([video["height"]*video["width"] for video in videos])
    _stats["min_height"] = min([video["height"] for video in videos])
    _stats["max_height"] = max([video["height"] for video in videos])
    _stats["min_width"] = min([video["width"] for video in videos])
    _stats["max_width"] = max([video["width"] for video in videos])
    
    
    tag = "length" if "length" in list(list(videos)[0].keys()) else "file_names"
    _stats["shortest_video"] = min([video[tag] if tag =="length" else len(video[tag]) for video in videos])
    _stats["longest_video"] = max([video[tag] if tag =="length" else len(video[tag]) for video in videos])
    _stats["average_video_length"] = np.mean([video[tag] if tag =="length" else len(video[tag])  for video in videos])
    
    return _stats



def get_areas_stats(tracks : list[dict] = []):
        """
        given annotations per track generate bounding boxes related insights
        """ 
        # coco and/or skydata areas sizes stats 
        _ranges_sizes = {'Micro':12**2, 
                        'Tiny':22**2,
                        'Small':32**2, 
                        'Medium':96**2, 
                        'Large':np.inf}
        boundaries = [0,*list(_ranges_sizes.values())]
        
        _stats = {
                    "areas_ranges": _ranges_sizes,
                    "areas_stats":defaultdict()
                }
        _sub_stats =  {
                        "min": [],
                        "max": [],
                        "mean": [],
                        "std": [],
                        "median": [],                        
                        'Micro':[], 
                        'Tiny':[],
                        'Small':[], 
                        'Medium':[], 
                        'Large':[]
                    }
        for track in tracks.values():
            
            annotations = track["bboxes"] if "bboxes" in track else track["segmentations"] if "segmentations" in track else track["areas"] if "areas" in track else []

            if type(annotations) == list and len(annotations) == 0:
                return {}
            assert len(annotations) > 0, "annotations should not be empty"

            if "areas" in track:
                boxes_areas = np.asarray([a for a in track["areas"] if a is not None]) 
            elif "bboxes" in track:
                # calculate areas manually
                boxes_areas = np.asarray([a[2]*a[3] for a in track["bboxes"] if a is not None])
            else:
                boxes_areas = np.asarray([])

            if len(boxes_areas) == 0:
                continue
            
            
            per_bin_counts , boundaries= np.histogram(boxes_areas, bins=boundaries)
            _area_ranges_stats = {str(k):v for k,v in zip(_ranges_sizes.keys(), per_bin_counts)}
            
            _sub_stats["min"].append(np.min(boxes_areas))
            _sub_stats["max"].append(np.max(boxes_areas))
            _sub_stats["mean"].append(np.mean(boxes_areas))
            _sub_stats["std"].append(np.std(boxes_areas))
            _sub_stats["median"].append(np.median(boxes_areas))
            
            for k,v in _area_ranges_stats.items():
                _sub_stats[k].append(v)
                
        #get means and max and min
        for k,v in _sub_stats.items():
            if k in ["min","max"]:
                _stats["areas_stats"][k] = eval(f"np.{k}(v)") if len(v) > 0 else 0
            elif k in ["mean","std","median"]:
                _stats["areas_stats"][k] = np.mean(v) if len(v) > 0 else 0              
            else:
                _stats["areas_stats"][k] = np.sum(v) if len(v) > 0 else 0
                
        del _sub_stats
        return _stats
