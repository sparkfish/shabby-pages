# This script generates the evaluation.csv file used to test the
# Denoising ShabbyPages Kaggle competition. It also generates a
# mapping.txt file showing the image order in the evaluation file
#
# To run it, you need a directory named "test", containing
# 300 PNG files of 500x500 pixels.

import os
import numpy as np
import cv2

with open("mapping.txt", "w") as log:
    with open("evaluation.csv", "w") as outfile:

        testfiles = sorted(os.listdir("/images/cropped/test_cleaned"))

        # the evaluation file contains pixel intensity data for the whole dataset,
        # in the following format:
        #     1_1_2,0
        # corresponding to the following data:
        # 1. which picture the data belongs to (filenum)
        # 2. the pixel's row img[j]
        # 3. the pixel's column img[,i]
        # 4. the intensity of the pixel (0 to 255 after grayscale)

        # Start counting files
        filenum = 1

        # Write the header to the evaluation file
        outfile.write("id,expected\n")

        # Process all the images
        for f in testfiles:
            if ".png" in f:
                # log the mapping between the filenum and image name
                log.write("{}: {}\n".format(filenum, f))

                # get the image
                img = cv2.imread("/images/cropped/test_cleaned/{}".format(f))

                # # make it grayscale so we can easily test RMSE
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # loop bounds
                y,x = img.shape

                # process the image pixel-by-pixel
                for j in range(y):
                    for i in range(x):
                        outfile.write("{}_{}_{},{}\n".format(filenum, j, i, img[j][i]/255.0))

                # increment the filenum since we're done with this image
                filenum = filenum + 1
