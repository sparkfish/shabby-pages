import os
import logging
import random
import tweepy

# Grab random image from daily build
filename = random.choice(os.listdir("cropped/shabby/"))
filename_upload = "cropped/shabby/" + filename
filename_display = os.path.splitext(filename)[0]

# Create tweet message
tweet = f"ShabbyPage-Of-The-Day w/ lastest Augraphy build for training #denoisers: {filename_display[0:20]}... "
tweet = tweet + "#ShabbyPages #Augraphy #ImageAugmentation #ComputerVision #OCR #TesseractOCR #OpenCV #DataAugmentation #binarization #doceng #MachineLearning #deeplearning"
logging.info(f"Tweet (len={str(len(tweet))}): "+tweet)

# Get secrets from environment
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

# Twitter API v1.1 client - for posting image media (until V2 supports images)
auth = tweepy.OAuthHandler( CONSUMER_KEY, CONSUMER_SECRET )
auth.set_access_token( ACCESS_TOKEN, ACCESS_TOKEN_SECRET )
api_v1 = tweepy.API(auth)
logging.info(f"Authenticated via V1 Twitter API; response = [{api_v1}]")

# Twitter API v2 client - for tweeting (cannot use v1.1 for tweeting with "Essential access" Developer account)
api_V2 = tweepy.Client(
    consumer_key = CONSUMER_KEY,
    consumer_secret = CONSUMER_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET
)
#user_info = api_V2.get_me() # call apparently blocked by "free" tier plan??
#logging.info(f"Authenticated via V2 Twitter API; connected as user `{user_info.data.username}`")

# Upload image
media = api_v1.media_upload(filename_upload)
logging.info(f"Media uploaded to twitter; response = [{media}]")

# Post tweet via V2 API w/ image's media id
try:
    # post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    post_result = api_V2.create_tweet(text=tweet, media_ids=[media.media_id])
    logging.info(f"Tweet posted referencing media upload; response = [{post_result}] ")
except Exception as e:
    print(e)
    print("Tweet is :"+tweet)
    print("Length of tweet is "+str(len(tweet)))    
    logging.error(e)
