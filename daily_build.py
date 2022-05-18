import cv2
import random
import os
import zipfile
from multiprocessing import Pool, cpu_count
from functools import partial
from daily_pipeline import get_pipeline
from remove_blank_pages import report_white_percentage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import gdown

def run_pipeline(filename):
    print(f"Processing {filename}")

    clean = cv2.imread(f"full/clean/{filename}")

    pipeline = get_pipeline()

    shabby = pipeline.augment(clean)["output"]

    if len(shabby.shape)<=2 and len(clean.shape)>2:
        shabby = cv2.cvtColor(shabby, cv2.COLOR_GRAY2BGR)

    left,right,top,bottom = choose_patch(clean)
    clean_patch = cv2.resize(clean[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)
    shabby_patch = cv2.resize(shabby[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    # add 38% of clean image patch into shabby image
    x_end_ratio_38_percent = int(400 * 38/100)
    shabby_patch[:, :x_end_ratio_38_percent] = clean_patch[:,:x_end_ratio_38_percent]
    
    # add line of gradient separating clean and shabby image
    gradient_value = 100
    for i in range(6):
        shabby_patch[:, x_end_ratio_38_percent - i] = gradient_value
        gradient_value += 30

    cv2.imwrite(f"full/shabby/{filename}", shabby)
    cv2.imwrite(f"cropped/clean/{filename}", clean_patch)
    cv2.imwrite(f"cropped/shabby/{filename}", shabby_patch)

    # select new patch when black area > 80% of the image
    while report_white_percentage(f"cropped/clean/{filename}")>99:
        os.remove(f"cropped/clean/{filename}")
        os.remove(f"cropped/shabby/{filename}")
    
        left,right,top,bottom = choose_patch(clean)
        clean_patch = cv2.resize(clean[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)
        shabby_patch = cv2.resize(shabby[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

        # add 38% of clean image patch into shabby image
        x_end_ratio_38_percent = int(400 * 38/100)
        shabby_patch[:, :x_end_ratio_38_percent] = clean_patch[:,:x_end_ratio_38_percent]
        
        # add line of gradient separating clean and shabby image
        gradient_value = 100
        for i in range(6):
            shabby_patch[:, x_end_ratio_38_percent - i] = gradient_value
            gradient_value += 30
        
        cv2.imwrite(f"cropped/clean/{filename}", clean_patch)
        cv2.imwrite(f"cropped/shabby/{filename}", shabby_patch)


def choose_patch(img):
    x,y,c = img.shape

    max_x = x - 500
    max_y = y - 500

    left = random.randint(0,max_x)
    top = random.randint(0,max_y)
    right = left + 500
    bottom = top + 500

    return left,right,top,bottom


def remove_blank_images(selected_images):
    filtered_images= []
    for filename in selected_images:
        # ensure image is not totally blank
        if report_white_percentage(f"full/clean/{filename}") <= 99:
            filtered_images.append(filename)
    return filtered_images


def download_images():
    # get the connection string for auth
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # create the BlobServiceClient object to mediate requests
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # create the ContainerClient object to manage the container
    container_client = blob_service_client.get_container_client(container="datasets")

    # get a generator with all the blobs in the container
    all_blobs = container_client.list_blobs()

    # select 50 blobs
    selected_blobs = random.sample(list(all_blobs), 10)

    # download the images
    for blob in selected_blobs:
        slug = blob.name[13:]
        thisfile = f"full/clean/{slug}"
        with open(thisfile, "wb") as outfile:
            print(f"Downloading {slug}")
            outfile.write(container_client.download_blob(blob).readall())

if __name__ == "__main__":

    # get the paper textures
    id = "1114s61-GmHbhIn8f9YNz6OwS3CwkOsIp"
    gdown.download(id=id, output="paper_textures.zip", quiet=True)

    # extract the zip
    with zipfile.ZipFile("paper_textures.zip", 'r') as zip_ref:
        zip_ref.extractall()

    # fix the directory name
    os.rename("paper textures", "paper_textures")

    # make working directories
    for directory in ["clean", "shabby"]:
        os.makedirs(f"full/{directory}")
        os.makedirs(f"cropped/{directory}")

    # download 50 random cleans to shabbify
    download_images()

    # get a list of the images
    selected_images = os.listdir("full/clean")

    # remove blank images
    selected_images = remove_blank_images(selected_images)

    # build process pool for parallel build
    num_cores = cpu_count()
    p = Pool(num_cores)

    # generate shabby pages
    p.map(run_pipeline, selected_images)
