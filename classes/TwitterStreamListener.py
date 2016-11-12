import datetime
import time
import tweepy

from twitter import TwitterStream
from twitter.stream import TwitterHTTPError, Timeout, HeartbeatTimeout, Hangup

try:
    import json
except ImportError:
    import simplejson as json


def log(entry, line=0):
    entry = entry.encode('ascii', errors='ignore')
    l = open("retweetbot.log", "a")
    timestamp = datetime.datetime.now().time()
    datestamp = datetime.datetime.now().date()
    if (line == 1):
        l.write("-----------------------------------------------------------\n\r")
    l.write(str(datestamp) + " " + str(timestamp) + ": " + entry + "\n\r")
    l.close()


class TwitterStreamListener:
    def getStatus(self):
        return "TwitterListener '" + self.name + "' Tracking: " + self.track

    def getName(self):
        return self.name

    def __init__(self, name, track, twitter_stream, tw_api, live, rtdb):
        self.name = name
        self.track = track
        self.tw_api = tw_api
        self.filterarray = []
        self.blacklist = []
        self.live = live
        self.counter = 151
        self.rtdb = rtdb

        # Initiate the connection to Twitter Streaming API
        self.twitter_stream = twitter_stream

    def addBlacklist(self, blacklist):
        self.blacklist = blacklist

    def setOauth(self, oauth):
        self.oauth = oauth

    def setCounter(self, counter):
        self.counter = counter

    def addfilter(self, filterarray):
        self.filterarray = filterarray

    def in_blacklist(self, dirty):

        for black in self.blacklist:

            if black.lower() in dirty.lower():
                return True

        return False

    def work(self):

        # Pull data from Twitter matching the query below:
        # Reference: https://dev.twitter.com/streaming/overview/request-parameters
        try:
            iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en", replies="all")
        except TwitterHTTPError, hx:
            log("Caught TwitterHTTPError for " + self.name)
            log("Trying again...")
            print("Caught TwitterHTTPError for " + self.name)
            print("Trying again...")
            log("The specific error is: " + str(hx))

            try:
                iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en", replies="all")
            except TwitterHTTPError, hx:
                log("Failed a second time for " + self.name)
                log("Killing of Thread...  :(")
                print("Failed a second time for " + self.name)
                print("Killing of Thread...  :(")
                log("The specific error is: " + str(hx))

        # Read and parse the tweets we find...

        tweet_count = self.counter
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
                log("(" + str(tweet_count) + "): Detected Hangup...")
                log("(" + str(tweet_count) +
                    "): Attempting to reconnect to TwitterStream...\n\r")
                time.sleep(300)
                self.twitter_stream = TwitterStream(auth=self.oauth)
                try:
                    time.sleep(300)
                    iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en", replies="all")
                except TwitterHTTPError, hx:
                    log("Caught TwitterHTTPError for " + self.name)
                    log("The specific error is: " + str(hx))

                log("(" + str(tweet_count) +
                    "): Successfully reconnected TwitterStream...\n\r")

                tweet_detail = "Hangup Recovery"
                continue

            if tweet_detail:
                log("(" + str(tweet_count) +
                    "): Ignoring Case: " + tweet_detail + "\n\r")

            tweettext = tweet['text']
            tweettext = tweettext.encode('ascii', errors='ignore')

            if self.in_blacklist(tweettext):
                log("Blacklist mention by " + tweet['user']['screen_name'] + ": " + tweettext)
                continue

            if self.in_blacklist(tweet['user']['screen_name']):
                log("Blacklisted Person (" + tweet['user']['screen_name'] + ") Tweet: " + tweettext)
                continue

            log("Identified Tweet " + self.name + " - (" + str(
                tweet_count) + "): Retweeting: " + str(
                tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))

            try:
                if tweet['retweeted_status']:
                    log("Retweet (" + str(tweet_count) + "):by: Screen Name: " +
                        tweet['retweeted_status']['user']['screen_name'])
                    log("Retweet (" + str(tweet_count) + "):by: Name: " +
                        tweet['retweeted_status']['user']['name'])
                    log("Retweet (" + str(tweet_count) + "):by: ID: " +
                        str(tweet['retweeted_status']['id']))
                    # log("Retweet Details: {}".format(tweet['retweeted_status']))

                    if self.rtdb.is_tweet_logged(tweet['retweeted_status']['id']):
                        log("Retweet (" + str(tweet_count) + "): This retweet is already recorded, continuing!")
                        continue
                    else:
                        self.rtdb.log_tweet(tweet['retweeted_status']['id'], "StreamListener-Retweet",
                                            tweet['retweeted_status']['user']['screen_name'])

            except KeyError, k:
                log("No Retweet Status")


            try:
                if len(self.filterarray) > 0:
                    tweeted = 0
                    for entry in self.filterarray:
                        # log("Testing to see if '" + entry + "' is in tweet '" + tweet[
                        # 'text'].lower() + "', and if so, retweeting...")
                        if entry in tweettext.lower():

                            if not self.rtdb.is_tweet_logged(tweet['id']):
                                log("Found keyword, retweeting: [id:" + str(tweet['id']) + " '" + tweettext + "'")

                                if self.live:
                                    self.rtdb.log_tweet(tweet['id'], "StreamListener", tweet['user']['screen_name'])
                                    self.tw_api.retweet(tweet['id'])

                            tweeted = 1
                            break;
                    if tweeted == 0:
                        log("Ignored tweet '" + tweettext + "'")
                else:

                    if not self.rtdb.is_tweet_logged(tweet['id']):

                        log("Unrestricted Tweet " + self.name + " - (" + str(
                            tweet_count) + ") <" + self.track + "> : Retweeting: " + str(
                            tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))
                        if self.live:
                            self.rtdb.log_tweet(tweet['id'], "StreamListener", tweet['user']['screen_name'])
                            self.tw_api.retweet(tweet['id'])

            except tweepy.error.TweepError, e:
                log("TweepError:  Just ignore it and move on with life...")
                log("The specific error is: " + str(e))
            if tweet_count <= 0:
                break
