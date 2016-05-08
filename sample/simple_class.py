print "Beginning of program"


class SimpleClass:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

sc1 = SimpleClass("Bob")
sc2 = SimpleClass("Bill")
sc3 = SimpleClass("Turkey")


print ("SC1:  "+sc1.getName())
print ("SC2:  "+sc2.getName())
print ("SC3:  "+sc3.getName())






print "Normal end of program"
