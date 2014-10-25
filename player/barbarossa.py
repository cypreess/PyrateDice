#!/usr/bin/env python

# Data
"""
{
    "players": [
        {
            "id": 0,
            "dice": 1,
            "name": "Player2"
        },
        {
            "id": 2,
            "dice": 1,
            "name": "Player1"
        }
    ],

    "gameplay": [
        #id, user_name, count, dice
        [0, "Player2", 1, 2]
    ],
    "dice": [3],
    "id": 2
}
"""

# cURL
# curl http://0.0.0.0:8000/bid -X POST -H "Content-Type: application/json" -d @data.json -w "\n"

# Get your bot name here
# http://www.piratequiz.com/

# Dirty Harry Rackham
#
# You're the pirate everyone else wants to throw
# in the ocean -- not to get rid of you, you understand;
# just to get rid of the smell. You have the good fortune
# of having a good name, since Rackham (pronounced RACKem,
# not rack-ham) is one of the coolest sounding surnames
# for a pirate. Arr!

from pirate import Pirate
import random
import json

def debug(message, data=None):
    print "DEBUG " + message + ": " + str(data)

class DirtyHarryRackham(Pirate):
    def do_bid(self, data):
        debug('input', data)

        players = data['players']
        gameplay = data['gameplay']
        dice = data['dice']

        try:
            last_bid = gameplay[-1][2:4]
        except IndexError:
            dice_count = len(dice)
            for player in players:
                dice_count += player['dice']

            bluff = self.start_game_with_bluff(dice, dice_count)
            debug('returning', bluff)

            return bluff

        players_count = len(players)

        iteration = len(data['gameplay'])
        if iteration > players_count/2:
            call = [0,0]
            debug('returning', call)
            return call
        else:
            bid_count, bid_dice = last_bid
            next_bid = [ bid_count+1, bid_dice ]
            debug('returning', next_bid)
            return next_bid

    def start_game_with_bluff(self, dice, dice_count):
        start_amount = 1
        end_amount = dice_count/2+1

        start_dice_amount_possibilities = range(start_amount, end_amount+1)
        debug('start_dice_amount_possibilities', start_dice_amount_possibilities)

        dice_amount = random.choice(start_dice_amount_possibilities)
        debug('dice_amount', dice_amount)

        dice_possibilities = range(1,7)
        bluff_dice = random.choice(dice_possibilities)
        debug('bluff_dice', bluff_dice)

        return [ dice_amount, bluff_dice ]


if __name__ == '__main__':
    DirtyHarryRackham().run()
