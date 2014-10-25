from pirate import Pirate
import json

def debug(message, data=None):
    print "DEBUG " + message + ": " + str(data)

class CptMorgan(Pirate):
    def do_bid(self, data):
        pass

if __name__ == '__main__':
    Pirate().run()
