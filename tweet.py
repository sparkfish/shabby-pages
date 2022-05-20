import os
import logging
import random
import tweepy

# Grab random image from daily build
filename_display = random.choice(os.listdir("cropped/shabby/"))
filename_upload = "cropped/shabby/" + filename_display

# Create tweet message
tweet = f"ShabbyPage-Of-The-Day using lastest build of Augraphy: {filename_display} "
tweet = tweet + "#ShabbyPages #Augraphy #ImageAugmentation #ComputerVision #OpenCV #DataAugmentation #MachineLearning #imgaug #albumentations #deeplearning #kaggle #ml #ai"

# Get secrets from environment
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Upload image
auth = tweepy.OAuthHandler( consumer_key, consumer_secret )
auth.set_access_token( access_token, access_token_secret )
api = tweepy.API(auth)
logging.info(f"Authenticated with Twitter API; response = [{api}]")

# Upload image
media = api.media_upload(filename_upload)
logging.info(f"Media uploaded to twitter; response = [{media}]")

# Post tweet with image
post_result = api.update_status(status=tweet, media_ids=[media.media_id])
logging.info(f"Tweet posted referencing media upload; response = [{post_result}] ")
