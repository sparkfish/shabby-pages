import os
import cv2
from multiprocessing import Pool
from pathlib import Path
from augraphy import *
from PIL import Image
import os
import random
import cv2
from glob import glob
import numpy as np
from daily_pipeline import get_pipeline

def run_pipeline(filename):
    image = cv2.imread(filename.as_posix())
    print(f"Processing {filename.stem}")
    # returns the current Shabby Pages pipeline
    pipeline = get_pipeline()
    data = pipeline.augment(image)
    shabby_image = data["output"]
    output_filename = f"shabby150/{filename.stem}.png"
    cv2.imwrite(output_filename, shabby_image)


if __name__ == "__main__":
    input_path = Path("clean150")
    filenames = [(input_path / name) for name in os.listdir(input_path)]

    pool = Pool(os.cpu_count())

    pool.imap_unordered(run_pipeline, filenames)
    # wait for everything to finish
    pool.close()
    pool.join()
