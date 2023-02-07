import os
from pathlib import Path
import cv2
import random
from multiprocessing import Pool
import sys
import numpy
import time

def generate_random_patch_coordinates(image):
    y,x,channels = image.shape
    patch_width = 400
    x_min = 0
    x_max = x - patch_width
    y_min = 0
    y_max = y - patch_width

    x1 = random.randint(x_min, x_max)
    y1 = random.randint(y_min, y_max)
    x2 = x1 + patch_width
    y2 = y1 + patch_width

    return x1,x2,y1,y2

def generate_ten_patches(filename_pair):
    print(f"Processing {filename_pair[0].as_posix()}")
    for i in range(10):
        clean_image = cv2.imread(filename_pair[0].as_posix())
        shabby_image = cv2.imread(filename_pair[1].as_posix())

        x_low,x_high,y_low,y_high = generate_random_patch_coordinates(clean_image)

        clean_patch = clean_image[x_low:x_high,y_low:y_high,:]
        shabby_patch = shabby_image[x_low:x_high,y_low:y_high,:]

        shabby_output_filename = 'patches/shabby_patches/' + filename_pair[0].stem + f'-patch-{i}.png'
        cv2.imwrite(shabby_output_filename, shabby_patch)

        clean_output_filename = 'patches/clean_patches/' + filename_pair[1].stem + f'-patch-{i}.png'
        cv2.imwrite(clean_output_filename, clean_patch)

if __name__ == '__main__':
    base_directory = Path('patches')
    base_directory.mkdir()
    shabby_full_directory = base_directory / 'shabby150'
    clean_full_directory = base_directory / 'clean150'

    shabby_patches_path = base_directory / 'shabby_patches'
    shabby_patches_path.mkdir()
    clean_patches_path = base_directory / 'clean_patches'
    clean_patches_path.mkdir()

    shabby_full_pages = [shabby_full_directory / filename for filename in sorted(os.listdir(shabby_full_directory))]
    clean_full_pages = [clean_full_directory / filename for filename in sorted(os.listdir(clean_full_directory))]

    filepath_pairs = zip(clean_full_pages, shabby_full_pages)

    process_pool = Pool(os.cpu_count())
    process_pool.imap_unordered(generate_ten_patches, filepath_pairs)
    # wait for everything to finish
    process_pool.close()
    process_pool.join()
