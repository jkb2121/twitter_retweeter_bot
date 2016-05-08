#!/usr/bin/python

import datetime
import threading
import time
import tweepy

from twitter import OAuth, TwitterStream
from twitter.stream import TwitterHTTPError, Timeout, HeartbeatTimeout, Hangup

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


def log(entry, line=0):
    entry = entry.encode('ascii', errors='ignore')
    l = open("retweetbot.log", "a")
    timestamp = datetime.datetime.now().time()
    datestamp = datetime.datetime.now().date()
    if (line == 1):
        l.write("-----------------------------------------------------------\n\r")
    l.write(str(datestamp) + " " + str(timestamp) + ": " + entry + "\n\r")
    l.close()


log("Starting Threaded Retweeter!", 1)

class TwitterListener:
    def getStatus(self):
        return "TwitterListener '" + self.name + "' Tracking: " + self.track

    def getName(self):
        return self.name

    def __init__(self, name, track, twitter_stream, tw_api):
        self.name = name
        self.track = track
        self.tw_api = tw_api
        self.filterarray = []
        self.blacklist = []

        # Initiate the connection to Twitter Streaming API
        self.twitter_stream = twitter_stream

        # Add @BrianBarganier to Blacklist
        self.blacklist.append("@BrianBarganier")

    def addfilter(self, filterarray):
        self.filterarray = filterarray

    def in_blacklist(self, dirty):

        for black in self.blacklist:

            if black.lower() in dirty.lower():
                return True

        return False

    def work(self):

        # Pull data from Twitter matching the query below:
        try:
            iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en")
        except TwitterHTTPError:
            log("Caught TwitterHTTPError for " + self.name)
            log("Trying again...")
            try:
                iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en")
            except TwitterHTTPError:
                log("Failed a second time for " + self.name)
                log("Killing of Thread...  :(")

        # Read and parse the tweets we find...

        tweet_count = 151
        for tweet in iterator:
            tweet_count -= 1

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
                log("(" + str(tweet_count) +
                    "): Ignoring Case: " + tweet_detail + "\n\r")

            tweettext = tweet['text']
            tweettext = tweettext.encode('ascii', errors='ignore')

            if self.in_blacklist(tweet['text']):
                log("Blacklist mention by " + tweet['user']['screen_name'] + ": " + tweettext)
                continue

            if self.in_blacklist(tweet['user']['screen_name']):
                log("Blacklisted Person (" + tweet['user']['screen_name'] + ") Tweet: " + tweettext)
                continue

            log("Identified Tweet " + self.name + " - (" + str(
                tweet_count) + "): Retweeting: " + str(
                tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))

            try:
                if len(self.filterarray) > 0:
                    tweeted = 0
                    for entry in self.filterarray:
                        # log("Testing to see if '" + entry + "' is in tweet '" + tweet[
                        # 'text'].lower() + "', and if so, retweeting...")
                        if entry in tweettext.lower():
                            log("Found keyword, retweeting: '" + tweettext + "'")
                            self.tw_api.retweet(tweet['id'])
                            tweeted = 1
                            break;
                    if tweeted == 0:
                        log("Ignored tweet '" + tweettext + "'")
                else:
                    log("Unrestricted Tweet " + self.name + " - (" + str(
                        tweet_count) + ") <" + self.track + "> : Retweeting: " + str(
                        tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))
                    self.tw_api.retweet(tweet['id'])
            except tweepy.error.TweepError:
                log("TweepError:  Just ignore it and move on with life...")

            if tweet_count <= 0:
                break

t1 = TwitterListener("#ctcomedy", "#ctcomedy", twitter_stream, tw_api)
log("TL1:" + t1.getStatus())

comics = "@apollojackson,@_Beecher_,@FunnyBone,@WichaelMeiss,@ryanbrauth,@comixmohegansun," + \
         "@DarrenSechrist,@jokesondrew,@Dannyboy3030,@DanRiceComedy,@Freudmayweather," + \
         "@RicenBeanJoker,@pat_oates,@GerriWulle,@ChrisClarke203,@APOLLOJACKSON,@JokerRome," + \
         "@KevinFitzComedy,@Ghostyfilms"

t2 = TwitterListener("Comics", comics, twitter_stream, tw_api)
log("TL2:" + t2.getStatus())

ft = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
ft.append("january")
ft.append("february")
ft.append("march")
ft.append("april")
ft.append("may")
ft.append("june")
ft.append("july")
ft.append("august")
ft.append("september")
ft.append("october")
ft.append("november")
ft.append("december")
t2.addfilter(ft)


# t3 = TwitterListener("TheRock", "#AddTheRockImproveAnything", twitter_stream, tw_api)
# t4 = TwitterListener("TonyAwards/MetGala", "#TonyAwards,#MetGala", twitter_stream, tw_api)
threads = []

t = threading.Thread(target=t1.work)
t.setDaemon(True)
threads.append(t)

t = threading.Thread(target=t2.work)
t.setDaemon(True)
threads.append(t)

# t = threading.Thread(target=t3.work)
# t.setDaemon(True)
# threads.append(t)

# t = threading.Thread(target=t4.work)
# t.setDaemon(True)
# threads.append(t)

try:
    for t in threads:
        t.start()

    log("Sleeping with a Join() so the daemons can work!")
    time.sleep(30)

    tc = 0
    for t in threads:
        log("Thread " + str(tc) + " Joining Thread..." + t.getName())
        tc += 1
    t.join()
# time.sleep(300)
except (KeyboardInterrupt, SystemExit):
    print "Detected Keyboard Interrupt!"
    log("Detected Keyboard Interrupt!")

log("Normal End of Program")
