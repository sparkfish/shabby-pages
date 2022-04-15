import os
import tweepy

# Connect to the Twitter API
token = os.environ.get("TWITTER_TOKEN")
auth = tweepy.Client(token)
api = tweepy.API(auth)

# Tweet a random image from the daily build
filename = random.choice(os.listdir("full/shabby/"))
message = f"Shabby Page Of The Day: {filename} #ShabbyPages #Augraphy"

# Just tweet it out
api.update_with_media(f"full/shabby/{filename}", status=message)
