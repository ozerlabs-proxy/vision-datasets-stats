"""
will contain functions for tracking (MOTS VIS MOT SOT ...) statistics. 

"""

import os
import sys
sys.path.append('../')

import json
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns