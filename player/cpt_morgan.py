from pirate import Pirate
import json

def debug(message, data=None):
    print "DEBUG " + message + ": " + str(data)

class CptMorgan(Pirate):
    def do_bid(self, data):
        '''
        data = {"players": [
                        {"id": 0, "dice": 1, "name": "Player2"},
                        {"id": 2, "dice": 1, "name": "Player1"}
                ],
                            #id, name, count, value
                "gameplay": [[0, "Player2", 1, 2]],
                #my_dices, my_id
                "dice": [3], "id": 2}
        '''
        players = data['players']
        gameplay = data['gameplay']
        dice = data['dice']

        try:
            last_bid = gameplay[-1][2:4]
        except IndexError:
            return

if __name__ == '__main__':
    Pirate().run()
