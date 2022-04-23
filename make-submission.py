import random
import os
import cv2

################################################################################
# CHANGE THIS
################################################################################
cleaned_images_dir = "path/to/your/cleaned/images"

################################################################################
# DON'T CHANGE ANYTHING BELOW HERE
################################################################################
def select_pixels(img):
    y,x = img.shape

    pixels = list()

    for i in range(10000):
        pixel = (random.randrange(y), random.randrange(x))

        if pixel not in pixels:
            pixels.append(pixel)

    return pixels

if __name__ == "__main__":
    random.seed(0)

    cleaned_images = sorted(os.listdir(cleaned_images_dir))

    with open("submission.csv", "w") as submission_file:
        submission_file.write("id,predicted\n")

        filenum = 1
        for image in cleaned_images:

            img = cv2.imread("{}/{}".format(cleaned_images_dir, image), cv2.IMREAD_GRAYSCALE)
            pixels = select_pixels(img)

            for pixel in pixels:
                y,x = pixel
                submission_file.write("{}_{}_{},{}\n".format(filenum, y, x, img[y][x]/255.0))

            filenum += 1
