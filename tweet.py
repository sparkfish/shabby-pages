import os
import sys
import random
import requests
import json

# Get a random image from the daily build
filename = "cropped/test/" + random.choice(os.listdir("cropped/test/"))

# Modify this if you like.
message = f"Shabby Page Of The Day: {filename} #ShabbyPages #Augraphy"

# Get secrets from environment
bearer_token = os.environ.get("TWITTER_TOKEN")
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")



# Upload the file
with open(filename, "rb") as upload_file:
    data = upload_file.read()
    resource_url ="https://upload.twitter.com/1.1/media/upload.json"

    upload_image = {
        "media": data,
        "media_category": "tweet_image"
    }

    image_headers = {
        "Authorization": "Bearer {}".format(bearer_token)
    }

    try:
        media_id=requests.post(resource_url,headers=image_headers,params=upload_image)
    except Exception as e:
        print(f"Failed: {e}")
        sys.exit()

# Assign metadata to the image
tweet_meta = {
    "media_id": media_id,
    "alt_text": {
        "text":"An image produced with the Augraphy library."
    }
}

metadata_url = "https://upload.twitter.com/1.1/media/metadata/create.json"
auth_data = {"grant_type": "client_credentials"}
metadata_resp = requests.post(metadata_url,params=tweet_meta,headers=auth_data)

print(metadata_resp.text)

# Build the tweet and send it
tweet = {"status": message, "media_ids": media_id}
post_url = "https://api.twitter.com/1.1/statuses/update.json"
post_resp = requests.post(post_url,params=tweet,headers=image_headers)
