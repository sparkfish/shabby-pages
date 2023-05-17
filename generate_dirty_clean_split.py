import os
import argparse
import glob
import cv2
import numpy as np
import random
from shabbypipeline import get_pipeline

def generate_split(image_path, output_path, seed=42):
    """ Main function to generate dirty images from shabby pipeline
    
    param image_path: Path of the input image folder.
    type image_path: string
    param output_path: Path of the outputs.
    type output_path: string
    param seed: Random seed of the augmentation.
    type seed: int, optional
    """
    
    # check for valid input image folder path
    if image_path is None or not os.path.isdir(image_path):
        print("Invalid input image folder!")
        return 
    # check for valid output image folder path
    if output_path is None or not os.path.isdir(output_path):
        print("Invalid output image folder!")
        return 

    # set random seed
    random.seed(seed)
    np.random.seed(seed)
    cv2.setRNGSeed(seed)
    
    image_paths = glob.glob(image_path+"/*")
    
    # create output directories
    clean_path = output_path + "/clean/"
    dirty_path = output_path + "/dirty/"
    os.makedirs(clean_path, exist_ok=True)
    os.makedirs(dirty_path, exist_ok=True)
    
    # retrieve shabby pipeline
    shabby_pipeline = get_pipeline()
    
    for i, image_path in enumerate(image_paths):
        
        # augment image
        image = cv2.imread(image_path)
        image_augmented = shabby_pipeline(image)
    
        # generate clean and dirty image path
        filename = os.path.basename(image_path)
        clean_output_path = clean_path + filename
        dirty_output_path = dirty_path + filename
        
        print("Processing image "+str(i)+" - "+filename)
        
        # write image to disk
        cv2.imwrite(clean_output_path, image)
        cv2.imwrite(dirty_output_path, image_augmented)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, help="Path of the input image folder")
    parser.add_argument("--output_path", type=str, help="Path of the outputs")
    parser.add_argument("--seed", type=int, default=42, help="Random seed of the augmentation")
    opt = parser.parse_args()

    generate_split(opt.image_path, opt.output_path, opt.seed)
