#!/usr/bin/python

import threading
import time
import tweepy

from twitter import OAuth, TwitterStream
from twitter.stream import TwitterHTTPError

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

# Configure the connections to Twitter with Python_twitter and Python_tweepy.
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
tw_api = tweepy.API(auth)


class TwitterListener:
    def __init__(self, name, track, twitter_stream, tw_api):
        self.name = name
        self.track = track
        self.tw_api = tw_api

        # Initiate the connection to Twitter Streaming API
        self.twitter_stream = twitter_stream

    def work(self):
        # for i in range (0, self.count+1):
        #    print "TwitterListener: " + self.name + ": " + str(i)
        #    time.sleep(self.sleep)

        # Pull data from Twitter matching the query below:
        try:
            iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en")
        except TwitterHTTPError:
            print "Caught TwitterHTTPError for " + self.name
            print "Trying again..."
            try:
                iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en")
            except TwitterHTTPError:
                print "Failed a second time for " + self.name
                print "Killing of Thread...  :("

        # Read and parse the tweets we find...

        tweet_count = 51
        for tweet in iterator:
            tweet_count -= 1

            tweettext = tweet['text']
            tweettext = tweettext.encode('ascii', errors='ignore')

            print ("Tweet " + self.name + " - (" + str(tweet_count) + ") <" + self.track + "> : Retweeting: " + str(
                tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))

            try:

                self.tw_api.retweet(tweet['id'])
            except tweepy.error.TweepError:
                print "Error:  Just ignore it and move on with life..."

            if tweet_count <= 0:
                break


# t1 = TwitterListener("MetGala", "#MetGala", twitter_stream, tw_api)

t2 = TwitterListener("TupacsMom", "MsAfeniShakur,AfeniShakur,Tupac", twitter_stream, tw_api)

# t3 = TwitterListener("TheRock", "#AddTheRockImproveAnything", twitter_stream, tw_api)
t4 = TwitterListener("TonyAwards/MetGala", "#TonyAwards,#MetGala", twitter_stream, tw_api)
threads = []

# t = threading.Thread(target=t1.work)
# t.setDaemon(True)
# threads.append(t)

t = threading.Thread(target=t2.work)
t.setDaemon(True)
threads.append(t)

# t = threading.Thread(target=t3.work)
# t.setDaemon(True)
# threads.append(t)

t = threading.Thread(target=t4.work)
t.setDaemon(True)
threads.append(t)

try:
    for t in threads:
        t.start()

    print "Sleeping for 300 seconds so the daemons can work!"
    time.sleep(300)
except (KeyboardInterrupt, SystemExit):
    print "Detected Keyboard Interrupt!"

print "Normal End of Program"
