print "Beginning of program"
import threading
import time

class Worker:
    def __init__(self, name, count, sleep):
        self.name = name
        self.sleep = sleep
        self.count = count


    def work(self):
        for i in range (0,self.count):
            print "Worker: " + self.name +": " + str(i) 
            time.sleep(self.sleep)



w1 = Worker("Bob", 20, 1)
#w1.work()

w2 = Worker("Turkey", 10,2)
#w2.work()

w3 = Worker("JimBob", 5,4)
#w3.work()


# Start Messing with some Threading:

workers = []

w = threading.Thread(target=w1.work)
w.setDaemon(True)
workers.append(w)

w = threading.Thread(target=w2.work)
w.setDaemon(True)
workers.append(w)

w = threading.Thread(target=w3.work)
w.setDaemon(True)
workers.append(w)


#workers.append(threading.Thread(target=w3.work))


try:
    for w in workers:
        w.start()

    print "OK, sleeping for 30 seconds so the daemons can do their thing!"
    time.sleep(30)
except (KeyboardInterrupt, SystemExit):
    print "Detected Keyboard Interrupt!"


print "Normal end of Program"
