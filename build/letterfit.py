import cv2
import numpy as np

class LetterFit():
    """Given a target DPI, a LetterFit object's `fit` method resizes
    or cuts a given image to fit a Letter page of that resolution.
    """

    def __init__(self, DPI=150):
        self.DPI = DPI
        self.xres = int(self.DPI*8.5)
        self.yres = int(self.DPI*11)

    def fit(self, fg):
        y,x,z = fg.shape

        if x > self.xres or y > self.yres:
            return self.crop_overlay(fg)
        else:
            return self.fit_overlay(fg)

    def crop_overlay(self, fg):
        y,x,z = fg.shape

        if y > self.yres:
            if x > self.xres:
                return fg[0:self.yres, 0:self.xres]
            else:
                img = np.zeros(shape=(self.yres,self.xres,3))
                img[0:self.yres,0:x] = fg[0:self.yres,0:x]
                return img
        else:
            img = np.zeros(shape=(self.yres,self.xres,3))
            img[0:y,0:self.xres] = fg[0:y,0:self.xres]
            return img

    def fit_overlay(self, fg):
        y,x,z = fg.shape

        scan = np.zeros(shape=(self.yres,self.xres,3))
        scan[0:y, 0:x] = fg
        return scan
