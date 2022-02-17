import os
import cv2

from multiprocessing import Pool
from samplegenerator import SampleGenerator


sg = SampleGenerator(150)

files = os.listdir()

def genfit(f):
    if "png" in f:
        img = cv2.imread(f)
        fit = sg.fit(img)
        filename = "fits/" + f[:-4] + "-fit.png"
        cv2.imwrite(filename, fit)

p = Pool(32)

p.map(genfit, files)
