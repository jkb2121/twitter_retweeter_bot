import datetime
import tweepy

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

    def __init__(self, name, track, twitter_stream, tw_api, live):
        self.name = name
        self.track = track
        self.tw_api = tw_api
        self.filterarray = []
        self.blacklist = []
        self.live = live
        self.counter = 151

        # Initiate the connection to Twitter Streaming API
        self.twitter_stream = twitter_stream

    def addBlacklist(self, blacklist):
        self.blacklist = blacklist

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
        try:
            iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en")
        except TwitterHTTPError:
            log("Caught TwitterHTTPError for " + self.name)
            log("Trying again...")
            print("Caught TwitterHTTPError for " + self.name)
            print("Trying again...")

            try:
                iterator = self.twitter_stream.statuses.filter(track=str(self.track), language="en")
            except TwitterHTTPError:
                log("Failed a second time for " + self.name)
                log("Killing of Thread...  :(")
                print("Failed a second time for " + self.name)
                print("Killing of Thread...  :(")

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

            if tweet['retweeted_status']:
                log("Retweet (" + str(tweet_count) + "):by: Screen Name: " +
                    tweet['retweeted_status']['user']['screen_name'])
                log("Retweet (" + str(tweet_count) + "):by: Name: " +
                    tweet['retweeted_status']['user']['name'])

            try:
                if len(self.filterarray) > 0:
                    tweeted = 0
                    for entry in self.filterarray:
                        # log("Testing to see if '" + entry + "' is in tweet '" + tweet[
                        # 'text'].lower() + "', and if so, retweeting...")
                        if entry in tweettext.lower():
                            log("Found keyword, retweeting: '" + tweettext + "'")
                            if self.live:
                                self.tw_api.retweet(tweet['id'])
                            tweeted = 1
                            break;
                    if tweeted == 0:
                        log("Ignored tweet '" + tweettext + "'")
                else:
                    log("Unrestricted Tweet " + self.name + " - (" + str(
                        tweet_count) + ") <" + self.track + "> : Retweeting: " + str(
                        tweet['user']['screen_name']) + ": " + tweettext + str("\n\r"))
                    if self.live:
                        self.tw_api.retweet(tweet['id'])
            except tweepy.error.TweepError:
                log("TweepError:  Just ignore it and move on with life...")

            if tweet_count <= 0:
                break
