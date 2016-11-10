import datetime
import time
import tweepy


def log(entry, line=0):
    entry = entry.encode('ascii', errors='ignore')
    l = open("retweetbot.log", "a")
    timestamp = datetime.datetime.now().time()
    datestamp = datetime.datetime.now().date()
    if (line == 1):
        l.write("-----------------------------------------------------------\n\r")
    l.write(str(datestamp) + " " + str(timestamp) + ": " + entry + "\n\r")
    l.close()


class TweepyWatcher:
    def __init__(self, name, api, live, rtdb):
        self.name = name
        self.watchlist = []
        self.filterlist = []
        self.api = api
        self.live = live
        self.counter = 10
        self.watchdelay = 15
        self.blacklist = []
        self.rtdb = rtdb

    def setCounter(self, counter):
        self.counter = counter

    def setWatchlist(self, watchlist):
        self.watchlist = watchlist

    def setFilter(self, filterlist):
        self.filterlist = filterlist

    def setWatchDelay(self, watchdelay):
        self.watchdelay = watchdelay

    def setBlacklist(self, blacklist):
        self.blacklist = blacklist

    def in_blacklist(self, dirty):

        for black in self.blacklist:

            if black.lower() in dirty.lower():
                return True

        return False

    def work(self):
        try:
            runcount = 0
            while True:
                for target in self.watchlist:
                    log("Target [" + str(runcount) + "]: " + str(target))

                    try:
                        t = 0
                        for status in self.api.user_timeline(target):
                            tweettext = status.text
                            tweettext = tweettext.encode('ascii', errors='ignore')

                            # log("Status (" + str(t) + "): " + str(tweettext))

                            if self.in_blacklist(tweettext):
                                log("Blacklist [" + str(runcount) + "] mention by " + str(target) + ": " + tweettext)
                                continue

                            for filter in self.filterlist:
                                if filter in status.text.lower():

                                    # if this tweet hasn't been logged yet, let's try to retweet it:
                                    if not self.rtdb.is_tweet_logged(status.id):

                                        log("Retweeting [" + str(runcount) + "][id:" + str(status.id) + "] (" + str(
                                            t) + "): " + str(tweettext))

                                        if self.live:
                                            self.rtdb.log_tweet(status.id, "TweepyWatcher")
                                            self.api.retweet(status.id)

                                            # self.api.retweet(status.id)
                            t += 1
                            if t > self.counter:
                                break
                    except tweepy.error.TweepError, e:
                        log("Caught Error[" + str(runcount) + "] with Target " + str(target) + "... Continuing.")
                        log("The specific error is: " + str(e))

                        continue

                time.sleep(self.watchdelay)
                runcount += 1

        except (KeyboardInterrupt, SystemExit):
            print "Detected Keyboard Interrupt!"
