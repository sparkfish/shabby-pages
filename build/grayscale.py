import cv2
import os
from multiprocessing import Pool

def make_grayscale(filename):
    if "png" in filename:
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        save_name = f[:-4] + "-gray.png"
        cv2.imwrite(save_name, gray)

if __name__ = "__main__":
    files = os.listdir()

    p = Pool(32)

    p.map(make_grayscale, files)
