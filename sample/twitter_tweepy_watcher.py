import time
import tweepy

from settings import ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)


class TweepyWatcher:
    def __init__(self, name, api):
        self.name = name
        self.watchlist = []
        self.filterlist = []
        self.api = api

    def setWatchlist(self, watchlist):
        self.watchlist = watchlist

    def setFilter(self, filterlist):
        self.filterlist = filterlist

    def work(self):
        try:
            while True:
                for target in self.watchlist:
                    print ("Target: " + str(target))

                    try:
                        t = 0
                        for status in api.user_timeline(target):
                            tweettext = status.text
                            tweettext = tweettext.encode('ascii', errors='ignore')

                            print "Status (" + str(t) + "): " + str(tweettext)

                            for filter in self.filterlist:
                                if filter in status.text.lower():
                                    print "Retweet!"

                            # api.retweet(status.id)
                            t += 1
                            if t > 10:
                                break
                    except tweepy.error.TweepError:
                        print "Caught Error with Target " + str(target) + "... Continuing."
                        continue

                time.sleep(15)

        except (KeyboardInterrupt, SystemExit):
            print "Detected Keyboard Interrupt!"


#

ft = ["the", "new", "coffee", "solo"]
targets = ['@midnight', '@hardwick', '@ComedyCentral', '@Ghostyfilms', '@starwars', '@startrek', '@starbucks']

tw1 = TweepyWatcher("Stars", api)
tw1.setWatchlist(targets)
tw1.setFilter(ft)
tw1.work()






# ft = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
# ft.append("january")
# ft.append("february")
# ft.append("march")
# ft.append("april")
# ft.append("may")
# ft.append("june")
# ft.append("july")
# ft.append("august")
# ft.append("september")
# ft.append("october")
# ft.append("november")
# ft.append("december")

# targets = ['@apollojackson','@_Beecher_','@FunnyBone','@WichaelMeiss','@ryanbrauth','@comixmohegansun',
#           '@DarrenSechrist','@jokesondrew','@Dannyboy3030','@DanRiceComedy','@Freudmayweather',
#           '@RicenBeanJoker','@pat_oates','@GerriWulle','@ChrisClarke203','@JokerRome',
#           '@KevinFitzComedy','@Ghostyfilms']
