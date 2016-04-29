#!/usr/bin/python

import datetime
import tweepy

from twitter import Twitter, OAuth, TwitterStream
from twitter.stream import Timeout, HeartbeatTimeout, Hangup

try:
    import json
except ImportError:
    import simplejson as json

try:
    from settings import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
except ImportError:
    print "Unable to import a settings.py file with the ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY and \n\r"
    print "CONSUMER_SECRET.  See the settings.py.sample file for details.\n\r"
    exit(1)

l = open("retweetbot.log", "a")
timestamp = datetime.datetime.now().time()
datestamp = datetime.datetime.now().date()
l.write("-----------------------------------------------------------\n\r")
l.write(str(datestamp) + " " + str(timestamp) + ": Starting Twitter_Retweeter_Bot\n\r")
l.close()

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

tweet_count = 51
for tweet in iterator:
    tweet_count -= 1

    # Write all the data we find to the logfile.
    f = open("retweetbot_debug.log", "a")
    l = open("retweetbot.log", "a")

    timestamp = datetime.datetime.now().time()
    datestamp = datetime.datetime.now().date()
    f.write("-----------------------------------------------------------\n\r")

    # Probably can do something more interesting with these, but I don't
    # quite know what yet.  So, let's just write them to the log, ignore
    # it, and then we'll see for next time...
    tweet_detail = 0
    if tweet is None:
        tweet_detail = "'None' reply"
    elif tweet is Timeout:
        tweet_detail = "Timeout"
    elif tweet is HeartbeatTimeout:
        tweet_detail = "Heartbeat Timeout"
    elif tweet is Hangup:
        tweet_detail = "Hangup"

    if tweet_detail:
        l.write(str(datestamp) + " " + str(timestamp) + "(" + str(tweet_count) +
                "): Ignoring Case: " + tweet_detail + "\n\r")

        # Maybe the right thing to do here would be to bump tweet_count back up to 51
        # and then maybe reestablish the twitter_stream and tw_api and restart
        # the iterator?
        continue

    # Get the ID of the Tweet and retweet it!
    try:

        tweettext = tweet['text']
        tweettext = tweettext.encode('ascii', errors='ignore')

        f.write(str(datestamp) + " " + str(timestamp) + "(" + str(tweet_count) + "): Retweeting: " + str(
            tweet['id']) + " from " + str(
            tweet['user']['screen_name']) + " " + tweettext + str("\n\r"))

        l.write(str(datestamp) + " " + str(timestamp) + "(" + str(tweet_count) + "): Retweeting: " + str(
            tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))

        f.write(json.dumps(tweet, indent=4))
        f.write("\n\r")

        # If you're testing, you can comment this out to not actually retweet
        tw_api.retweet(tweet['id'])

    except tweepy.error.TweepError:
        f.write(str(datestamp) + " " + str(timestamp) + "(" + str(
            tweet_count) + "): Error:  Just ignore it and move on with life....\n\r")
        l.write(str(datestamp) + " " + str(timestamp) + "(" + str(
            tweet_count) + "): Error: Already Tweeted prior tweet, continuing...\n\r")

    l.close()
    f.close()

    # Break if we hit the threshold

    if tweet_count <= 0:
        break

l = open("retweetbot.log", "a")
timestamp = datetime.datetime.now().time()
datestamp = datetime.datetime.now().date()
l.write(str(datestamp) + " " + str(timestamp) + ": Normal End of Program: Twitter_Retweeter_Bot")
l.close()
