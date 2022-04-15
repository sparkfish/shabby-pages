import cv2
import random
import os
import shutil
from functools import partial
from daily_pipeline import get_pipeline
from azure_file_service import Storage
import gdown

if __name__ == "__main__":

    # get the paper textures
    url = "https://drive.google.com/drive/folders/1NZ9t1jcyIIjc4fPjhBZYVWa0a27eg0AD"
    gdown.download_folder(url, quiet=True, use_cookies=False)

    # make working directories
    for directory in ["clean", "shabby"]:
        os.makedirs(f"full/{directory}")
        os.makedirs(f"cropped/{directory}")

    # connect to Azure File Service
    afs = Storage()

    # pick and download 50 images
    all_files = afs.list_all_files()
    sampled_files = random.sample(all_files, 50)
    get_file = partial(afs.download_file, directory="full/clean")
    map(get_file, sampled_files)

    # get the downloaded images
    sampled_files = map(cv2.imread, os.listdir("full/clean"))

    # generate shabby pages
    map(run_pipeline, sampled_files)

def run_pipeline(filename):
    print(f"Processing {f}")

    clean = cv2.imread(f"full/clean/{filename}")

    pipeline = get_pipeline()

    shabby = pipeline.augment(clean)["output"]

    left,right,top,bottom = choosePatch(clean)

    clean_patch = cv2.resize(clean[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    shabby_patch = cv2.resize(shabby[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    shutil.copyfile(f"150dpi/{filename}", f"full/clean/{filename}")
    cv2.imwrite(f"full/shabby/{filename}", shabby)
    cv2.imwrite(f"cropped/clean/{filename}", clean_patch)
    cv2.imwrite(f"cropped/shabby/{filename}", shabby_patch)


def choosePatch(img):
    x,y,c = img.shape

    max_x = x - 500
    max_y = y - 500

    left = random.randint(0,max_x)
    top = random.randint(0,max_y)
    right = left + 500
    bottom = top + 500

    return left,right,top,bottom
