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
    def __init__(self, name, api, live):
        self.name = name
        self.watchlist = []
        self.filterlist = []
        self.api = api
        self.live = live
        self.counter = 10
        self.watchdelay = 15
        self.blacklist = []

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
            while True:
                for target in self.watchlist:
                    log("Target: " + str(target))

                    try:
                        t = 0
                        for status in self.api.user_timeline(target):
                            tweettext = status.text
                            tweettext = tweettext.encode('ascii', errors='ignore')

                            log("Status (" + str(t) + "): " + str(tweettext))

                            if self.in_blacklist(tweettext):
                                log("Blacklist mention by " + str(target) + ": " + tweettext)
                                continue

                            for filter in self.filterlist:
                                if filter in status.text.lower():
                                    log("Retweet!")

                                    if self.live:
                                        self.api.retweet(status.id)
                            t += 1
                            if t > self.counter:
                                break
                    except tweepy.error.TweepError:
                        log("Caught Error with Target " + str(target) + "... Continuing.")
                        continue

                time.sleep(self.watchdelay)

        except (KeyboardInterrupt, SystemExit):
            print "Detected Keyboard Interrupt!"
