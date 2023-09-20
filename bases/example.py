"""
Dataset toy example to test functionality of the framework.
"""

from .base_dataset_functionality import BaseDataset

class Example(BaseDataset):
    
    def __init__(self):
        extra_tags = ['extra_tag1', 'extra_tag2']
        super().__init__(extra_tags=extra_tags)

        # create the index
        self.create_index()

    def create_index(self):
        """
            Depending on the dataset we might need to create an index for the dataset.
            for faster access to the data attributes and labels.
        """
        print(f"[INFO] Creating index for the {self.__class__.__name__}...")
        # create index here

        print(f"[INFO] Index created for the {self.__class__.__name__}.")

    def generate_dataset_statistics(self):

        '''
            This function generates the dataset statistics. including: counts.
            The statistics are saved in a dictionary with keys as the tags and values as the statistics.
        '''
        print(f"[INFO] Generating dataset statistics for the {self.__class__.__name__}...")
        
        self.dataset_statistics['dataset_name'] = 'Example'
        self.dataset_statistics['dataset_size'] = 100
        self.dataset_statistics['dataset_classes'] = 10
        self.dataset_statistics['description'] = 'Example dataset'
        self.dataset_statistics['created_by'] = 'Example'
        self.dataset_statistics['extra_tag1'] = 'extra_tag1'
        self.dataset_statistics['extra_tag2'] = 'extra_tag2'

        print(f"[INFO] Dataset statistics generated for the {self.__class__.__name__}.")

