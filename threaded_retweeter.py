import sys
import threading
import time
import tweepy

import yaml
from twitter import OAuth, TwitterStream

from classes.TweepyWatcher import TweepyWatcher
from classes.TwitterStreamListener import TwitterStreamListener

# TODO Set up Logging
# TODO Perpetual Mode



if len(sys.argv) != 2:
    print "Usage threaded_retweeter.py <config>.yaml"
    exit(1)

print "Using Configuration File: " + sys.argv[1]
filename = sys.argv[1]

try:
    with open(filename, 'r') as f:
        yml = yaml.load(f)
except IOError:
    print "Error Opening Config File: " + filename
    exit(1)

TwitterAccount = yml['twitter_account']['account_name']
ACCESS_TOKEN = yml['twitter_account']['ACCESS_TOKEN']
ACCESS_SECRET = yml['twitter_account']['ACCESS_SECRET']
CONSUMER_KEY = yml['twitter_account']['CONSUMER_KEY']
CONSUMER_SECRET = yml['twitter_account']['CONSUMER_SECRET']

# print "Twitter Account: " + TwitterAccount
# print "Access Token: " + ACCESS_TOKEN
# print "Access Secret: " + ACCESS_SECRET
# print "Consumer Key: " + CONSUMER_KEY
# print "Consumer Secret: " + CONSUMER_SECRET
# print ""
# print str(yml)

# Configure the connections to Twitter with Python_twitter and Python_tweepy.
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)
tw_api = tweepy.API(auth)

blacklist = []
for bl in yml['blacklist']:
    # print "Blacklist: " + yml['blacklist'][bl]
    blacklist.append(str(yml['blacklist'][bl]))

threads = []

try:
    for st in yml['stream_retweeter']:
        # print "Stream Retweeter: " + str(st)

        # print "Stream: " + str(yml['stream_retweeter'][str(st)])

        name = str(yml['stream_retweeter'][str(st)]['name'])
        livetweet = yml['stream_retweeter'][str(st)]['livetweet']
        counter = yml['stream_retweeter'][str(st)]['counter']

        delim = ''
        stream = ''
        for watchwords in yml['stream_retweeter'][str(st)]['stream']:
            stream = yml['stream_retweeter'][str(st)]['stream'][watchwords] + delim + stream
            delim = ','
            # print "-" + stream + "\n\r"

        ts = TwitterStreamListener(name, stream, twitter_stream, tw_api, livetweet)

        k = []
        try:
            for keywords in yml['stream_retweeter'][str(st)]['keywords']:
                # print "Keyword: " + yml['stream_retweeter'][str(st)]['keywords'][keywords]
                k.append(str(yml['stream_retweeter'][str(st)]['keywords'][keywords]))
        except TypeError:
            k = []

        ts.addfilter(k)
        ts.setCounter(counter)
        ts.addBlacklist(blacklist)

        t = threading.Thread(target=ts.work)
        t.setDaemon(True)
        threads.append(t)
except KeyError:
    print "No Stream Retweeters In Config"

try:
    for st in yml['watcher']:

        name = str(yml['watcher'][str(st)]['name'])
        livetweet = yml['watcher'][str(st)]['livetweet']
        counter = yml['watcher'][str(st)]['counter']
        watchdelay = yml['watcher'][str(st)]['watchdelay']

        w = []
        for watching in yml['watcher'][str(st)]['watching']:
            # print "Watching: " + yml['watcher'][str(st)]['watching'][watching]
            w.append(str(yml['watcher'][str(st)]['watching'][watching]))

        k = []
        for keywords in yml['watcher'][str(st)]['keywords']:
            # print "Keyword: " + yml['watcher'][str(st)]['keywords'][keywords]
            k.append(str(yml['watcher'][str(st)]['keywords'][keywords]))

        tw1 = TweepyWatcher(name, tw_api, livetweet)
        tw1.setWatchlist(w)
        tw1.setFilter(k)
        tw1.setWatchDelay(watchdelay)
        tw1.setBlacklist(blacklist)

        t = threading.Thread(target=tw1.work)
        t.setDaemon(True)
        threads.append(t)

except KeyError:
    print "No TweepyWatchers In Config"

try:
    for t in threads:
        t.start()

    print ("Sleeping with a Join() so the daemons can work!")
    print ("Twitter output being sent to the log file.")
    time.sleep(60)

    tc = 0
    for t in threads:
        print ("Thread " + str(tc) + " Joining Thread..." + t.getName())
        tc += 1
    t.join()
# time.sleep(300)
except (KeyboardInterrupt, SystemExit):
    print "Detected Keyboard Interrupt!"
