import os
import cv2
import random
import numpy as np
from functools import partial
from multiprocessing import Pool


def report_white_percentage(filename):
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    binarized = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]/255.0

    y,x = binarized.shape

    white_pixels = np.sum(binarized)

    white_percentage = 100 * white_pixels / (y * x)

    return white_percentage

def prepend_path(path, filename):
    return path + filename

if __name__ == "__main__":

    train_images = os.listdir("cropped/train")
    train_cleaned_images = os.listdir("cropped/train_cleaned")
    test_images = os.listdir("cropped/test")
    test_cleaned_images = os.listdir("cropped/test_cleaned")

    def remove_train_whites(img):
        shabbypath = f"cropped/train/{img}"
        cleanpath = f"cropped/train_cleaned/{img}"

        if report_white_percentage(shabbypath) > 99:
            print(f"Removing {img}")
            os.remove(shabbypath)
            os.remove(cleanpath)

    def remove_test_whites(img):
        shabbypath = f"cropped/test/{img}"
        cleanpath = f"cropped/test_cleaned/{img}"

        if report_white_percentage(shabbypath) > 99:
            print(f"Removing {img}")
            os.remove(shabbypath)
            os.remove(cleanpath)

    p = Pool(32)

    p.map(remove_train_whites, train_images)
    p.map(remove_test_whites, test_images)
