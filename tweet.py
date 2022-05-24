import os
import logging
import random
import tweepy

# Grab random image from daily build
filename = random.choice(os.listdir("cropped/shabby/"))
filename_upload = "cropped/shabby/" + filename
filename_display = os.path.splitext(filename)[0]

# Create tweet message
tweet_filename = f"ShabbyPage-Of-The-Day using lastest build of Augraphy: {filename_display} "
tweet = tweet_filename + "#ShabbyPages #Augraphy #ImageAugmentation #ComputerVision #OpenCV #DataAugmentation #MachineLearning #imgaug #albumentations #deeplearning #kaggle #ml #ai"

# Get secrets from environment
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# Authenticate API user
auth = tweepy.OAuthHandler( consumer_key, consumer_secret )
auth.set_access_token( access_token, access_token_secret )
api = tweepy.API(auth)
logging.info(f"Authenticated with Twitter API; response = [{api}]")

# Upload image
media = api.media_upload(filename_upload)
logging.info(f"Media uploaded to twitter; response = [{media}]")

# Post tweet with image
try:
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    logging.info(f"Tweet posted referencing media upload; response = [{post_result}] ")
except Exception as e: 
    print(e)
    print("Length of tweet is "+len(tweet))
    print("Tweet is :"+tweet)
    
