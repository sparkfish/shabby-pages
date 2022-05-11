import os
import sys
import random
import requests
import json
import base64
# Get a random image from the daily build
filename = "cropped/test/" + random.choice(os.listdir("cropped/test/"))

# Modify this if you like.
message = f"Shabby Page Of The Day: {filename} #ShabbyPages #Augraphy"

# Get secrets from environment
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


#Reformat the keys and encode them
key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
#Transform from bytes to bytes that can be printed
b64_encoded_key = base64.b64encode(key_secret)
#Transform from bytes back into Unicode
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
access_token = auth_resp.json()['access_token']


# Upload the file
with open(filename, "rb") as upload_file:
    data = upload_file.read()
    resource_url ="https://upload.twitter.com/1.1/media/upload.json"

    upload_image = {
        "media": data,
        "media_category": "tweet_image"
    }

    image_headers = {
        "Authorization": "Bearer {}".format(access_token)
    }

    try:
        media_id=requests.post(resource_url,headers=image_headers,data=upload_image)
        print(media_id.json())
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