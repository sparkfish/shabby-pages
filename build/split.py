import os
import cv2
import random
import numpy as np
from augraphy import *
from multiprocessing import Pool

import shutil

random.seed(0)
np.random.seed(0)


cleans = os.listdir("cropped/clean")

train_split = random.sample(cleans, 700)

def trainSplit(filename):
    if filename in train_split:
        return True
    else:
        return False

def split(filename):
    outputdir = "train" if trainSplit(filename) else "test"

    if outputdir == "train":
        shutil.copy("cropped/clean/" + filename, "train_cleaned/")
        shutil.copy("cropped/shabby/" + filename, "train/")
    else:
        shutil.copy("cropped/clean/" + filename, "test_cleaned/")
        shutil.copy("cropped/shabby/" + filename, "test/")

p = Pool(32)

p.map(split, cleans)
