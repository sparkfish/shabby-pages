import cv2
import random
import os
import zipfile
from multiprocessing import Pool, cpu_count
from functools import partial
from daily_pipeline import get_pipeline
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import gdown

def run_pipeline(filename):
    print(f"Processing {filename}")

    clean = cv2.imread(f"full/clean/{filename}")

    pipeline = get_pipeline()

    shabby = pipeline.augment(clean)["output"]

    left,right,top,bottom = choosePatch(clean)

    clean_patch = cv2.resize(clean[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    shabby_patch = cv2.resize(shabby[left:right,top:bottom], (400,400), interpolation = cv2.INTER_AREA)

    cv2.imwrite(f"full/shabby/{filename}", shabby)
    cv2.imwrite(f"cropped/clean/{filename}", clean_patch)
    cv2.imwrite(f"cropped/shabby/{filename}", shabby_patch)


def choosePatch(img):
    x,y,c = img.shape

    max_x = x - 500
    max_y = y - 500

    left = random.randint(0,max_x)
    top = random.randint(0,max_y)
    right = left + 500
    bottom = top + 500

    return left,right,top,bottom

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
    selected_blobs = random.sample(list(all_blobs), 50)

    # download the images
    for blob in selected_blobs:
        slug = blob.name[13:]
        thisfile = f"full/clean/{slug}"
        with open(thisfile, "wb") as outfile:
            print(f"Downloading {slug}")
            outfile.write(container_client.download_blob(blob).readall())

if __name__ == "__main__":

    # get the paper textures
    id = "1114s61-GmHbhIn8f9YNz6OwS3CwkOsIp&authuser=0"
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

    # build process pool for parallel build
    num_cores = cpu_count()
    p = Pool(num_cores)

    # generate shabby pages
    p.map(run_pipeline, selected_images)
