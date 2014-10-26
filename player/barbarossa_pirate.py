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

import random

from pirate import Pirate


def debug(message, data=None):
    print "DEBUG " + message + ": " + str(data)


class Barbarossa(Pirate):
    def do_bid(self, data):
        # debug('input', data)
        debug('--- NEW BID ---')

        players = data['players']
        gameplay = data['gameplay']
        dice = data['dice']
        debug('dice', dice)

        dice_count = len(dice)

        new_game = False

        try:
            last_bid = gameplay[-1][2:4]
            bid_count, bid_dice = last_bid
        except IndexError:
            new_game = True

        if new_game or bid_dice == 0:
            for player in players:
                debug('player dice', player['dice'])
                dice_count += player['dice']

            bluff = self.start_game_with_bluff(dice, dice_count)
            debug('bluff return', bluff)

            return bluff

        players_count = len(players)

        tolerance_list = [4, 5, 6, 7, 8]
        tolerance = random.choice(tolerance_list)

        iteration = len(data['gameplay'])
        if iteration > players_count / 2 + tolerance:
            call = [0, 0]
            debug('iteration call', call)
            debug('iteration (is >)', iteration)
            debug('players_count (divide by 2)', players_count)
            debug('tolerance (add to players_count)', tolerance)
            return call
        else:
            next_bid_count = bid_count + 1
            if next_bid_count >= dice_count:
                call = [0, 0]
                debug('edge call', call)
                debug('next_bid_count (is >)', next_bid_count)
                debug('dice_count', dice_count)
                return call

            next_bid = [next_bid_count, bid_dice]
            debug('bid return', next_bid)
            return next_bid

    def start_game_with_bluff(self, dice, dice_count):
        start_amount = 1
        end_amount = dice_count / 2 + 1

        start_dice_amount_possibilities = range(start_amount, end_amount + 1)
        debug('start_dice_amount_possibilities', start_dice_amount_possibilities)

        dice_amount = random.choice(start_dice_amount_possibilities)
        debug('dice_amount', dice_amount)

        dice_possibilities = range(1, 7)
        bluff_dice = random.choice(dice_possibilities)
        debug('bluff_dice', bluff_dice)

        return [dice_amount, bluff_dice]


if __name__ == '__main__':
    Barbarossa().run()
