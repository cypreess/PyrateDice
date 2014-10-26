#!/usr/bin/env python
from collections import Counter

from pirate import Pirate

# Example input
# {"players": [{"id": 0, "dice": 1, "name": "Player2"}, {"id": 2, "dice": 1, "name": "Player1"}], "gameplay": [[0, "Player2", 1, 2]], "dice": [3], "id": 2}

class CrimsonPirate(Pirate):
    def do_bid(self, data):
        total_dice = sum([x['dice'] for x in data['players']])
        last_user_id, last_user_name, last_count, last_die = None, None, None, None
        if len(data['gameplay']):
            last_user_id, last_user_name, last_count, last_die = data['gameplay'][-1]

        best_options = Counter(data['dice']).most_common()
        best_options = [x for x in best_options if x[1] == best_options[0][1]]
        best_options = sorted(best_options, key=lambda x: x[0], reverse=True)

        best = (best_options[0][1], best_options[0][0])

        if last_count is None or last_count == 0:
            return best
        else:
            if best[0] > last_count:
                    return best
            if best[0] == last_count:
                if best[1] > last_die:
                    return best
            if best[0] + 1 > last_count or (best[0] + 1 == last_count and best[1] > last_die):
                return best[0] +1, best[1]

            return 0, 0


if __name__ == '__main__':
    CrimsonPirate().run()