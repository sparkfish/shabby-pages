import time
import os
import cv2

from multiprocessing import Pool
from crappify import gen_pipeline

directories = ["150dpi", "300dpi", "600dpi", "1200dpi"]

dir_files = dict()

for imdir in directories:
    dir_files[imdir] = sorted(os.listdir(imdir))

for i in range(100):
    pipeline = gen_pipeline()

    output = str(i) + " "

    for imdir in directories:
        imname = dir_files[imdir][i]
        img = cv2.imread(imdir + "/" + imname)
        start = time.time()
        crappified = pipeline.augment(img)["output"]
        stop = time.time()
        duration = stop - start
        save_name = ("crappified/" + imdir + "/" + imname[:-4] + "-augraphy-" + imdir + ".png")
        cv2.imwrite(save_name, crappified)
        output += (imdir + ": " + str(duration) + " ")

    print(output)
