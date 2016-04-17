#!/usr/bin/python

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import tweepy
import datetime
try:
    import json
except ImportError:
    import simplejson as json

try:
    from settings import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
except ImportError:
    print "Unable to import a settings.py file with the ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY and CONSUMER_SECRET.  See the settings.py.sample file for details."
    exit(1)


# Configure the connections to Twitter with Python_twitter and Python_tweepy.
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
t = Twitter(auth=oauth)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
tw_api = tweepy.API(auth)


# Pull data from Twitter matching the query below:
iterator = twitter_stream.statuses.filter(track="#ctcomedy", language="en")


# Read and parse the tweets we find...

tweet_count = 50
for tweet in iterator:
    tweet_count -= 1

    # Write all the data we find to the logfile.
    f = open ("retweetbot.log","a")

    # Get the ID of the Tweet and Retweet it!
    try:
        timestamp = datetime.datetime.now().time()
        datestamp = datetime.datetime.now().date()

        f.write("-----------------------------------------------------------\n\r")
        f.write(str(datestamp) + " " + str(timestamp) + ": Retweeting: "+str(tweet['id'])+" from "+str(tweet['user']['screen_name'])+":\n\r")
        f.write(json.dumps(tweet,indent=4))
        f.write("\n\r")

        # If you're testing, you can comment this out to not actually retweet
        tw_api.retweet(tweet['id'])

    except tweepy.error.TweepError:
        f.write("Error:  Just ignore it and move on with life....\n\r")

    f.close()

    # Break if we hit the threshold

    if tweet_count <= 0:
        break 








