import cv2
import random
import os
import shutil
from multiprocessing import Pool, cpu_count
from daily_pipeline import get_pipeline

################################################################################
# Create directories
################################################################################
for directory in ["train", "train_cleaned", "test", "test_cleaned"]:
    os.makedirs(f"/images/full/{directory}")
    os.makedirs(f"/images/cropped/{directory}")

################################################################################
# Get clean full document images
################################################################################
all_images = os.listdir("/images/150dpi")

################################################################################
# Randomly select num_cleans images to get shabby'd
################################################################################
num_cleans = 1500
num_trains = int(num_cleans*0.7)
full_cleans = random.sample(all_images, num_cleans)
trains = random.sample(full_cleans, num_trains)

def trainSplit(filename):
    if filename in trains:
        return True
    else:
        return False

def choosePatch(img):
    x,y,c = img.shape

    max_x = x - 500
    max_y = y - 500

    left = random.randint(0,max_x)
    top = random.randint(0,max_y)
    right = left + 500
    bottom = top + 500

    return left,right,top,bottom

def run_pipeline(filename):
    outputdir = "/images/train" if trainSplit(filename) else "/images/test"

    print("Processing {} as {}".format(filename, outputdir.split("/")[2]))
    clean = cv2.imread(f"/images/150dpi/{filename}")

    pipeline = get_pipeline()

    shabby = pipeline.augment(clean)["output"]

    left,right,top,bottom = choosePatch(clean)

    clean_patch = cv2.resize(clean[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    shabby_patch = cv2.resize(shabby[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    if outputdir == "/images/train":
        shutil.copyfile("/images/150dpi/{}".format(filename), "/images/full/train_cleaned/{}".format(filename))
        cv2.imwrite("/images/full/train/{}".format(filename), shabby)
        cv2.imwrite("/images/cropped/train_cleaned/{}".format(filename), clean_patch)
        cv2.imwrite("/images/cropped/train/{}".format(filename), shabby_patch)
    else:
        shutil.copyfile("/images/150dpi/{}".format(filename), f"/images/full/test_cleaned/{filename}")
        cv2.imwrite("/images/full/test/{}".format(filename), shabby)
        cv2.imwrite("/images/cropped/test_cleaned/{}".format(filename), clean_patch)
        cv2.imwrite("/images/cropped/test/{}".format(filename), shabby_patch)

num_cores = cpu_count()
p = Pool(num_cores)

p.map(run_pipeline, full_cleans, chunksize=10)
