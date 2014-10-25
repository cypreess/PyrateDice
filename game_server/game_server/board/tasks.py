from __future__ import absolute_import
from copy import deepcopy
from itertools import cycle
import json
from random import randrange

from celery import shared_task
from celery.utils.log import get_task_logger
import requests
from requests.exceptions import ReadTimeout

from board.models import BoardState

logger = get_task_logger(__name__)

MAX_DICE = 5


class GameError(Exception):
    pass


def get_move(url, data):
    count = None
    die = None
    message = None

    try:
        response = requests.post(url, data=data, timeout=1)
    except ReadTimeout:
        raise GameError('Bid timeout')
    except Exception, e:
        raise GameError('Connection error: %s' % e)

    try:
        response_json = json.loads(response.text)
    except:
        raise GameError('Bid response is not in json format')

    try:
        count, die = response_json
        count = int(count)
        die = int(die)
    except:
        raise GameError('Bid is not in format (int(count), int(die))')
    return count, die


def check_move(count, die, gameplay, dice_count):
    if not ((count == 0 and die == 0) or (count > 0 and die >= 1 and die <= 6)):
        raise GameError('Bid must be (0, 0) or ( >0 , 1..6 )')
    if count == 0 and die == 0 and len(gameplay) == 0:
        raise GameError('Cannot call as the first player')

    if count > dice_count:
        raise GameError('Too high bid')

    if gameplay:
        player_id, player_name, last_count, last_die = gameplay[-1]
        if not (count > last_count or (count == last_count and die > last_die)):
            raise GameError('Bid is lower than last bid=(%d, %d)' % (last_count, last_die))


@shared_task
def board_iteration(iteration):

    logger.warning("Entering iteration %d" % iteration)
    if not BoardState.objects.filter(iteration=iteration).exists():
        if not BoardState.objects.filter(iteration=iteration - 1).exists():
            logger.error("Previous iteration %d not exists (and it should not)" % iteration)
            return

        last_game_state = BoardState.objects.get(iteration=iteration - 1)

        board_data = last_game_state.board_data
        state_data = last_game_state.state_data

        print "BOARD_DATA=%s" % board_data
        print "STATE_DATA=%s" % state_data


        board_data[u'message'] = ""

        if board_data[u'last_player'] is None:
            next_player = 0
            # initialize new dice for new game

            for player in state_data['players']:
                if board_data['players'][player['id']]['active']:
                    board_data['players'][player['id']]['dice'] = []
                    for i in range(player['dice']):
                        board_data['players'][player['id']]['dice'].append(randrange(1, 6))
                else:
                    board_data['players'][player['id']]['dice'] = []

        else:
            players_queue = cycle(board_data[u'players'])
            for i in xrange(board_data[u'last_player']+1):
                players_queue.next()

            for player_candidate in players_queue:
                if player_candidate['active']:
                    next_player = player_candidate['id']
                    break

        print "NEXT PLAYER = %d " % next_player

        player_id = next_player
        player_name = board_data[u'players'][next_player]['name']
        player_url = board_data[u'players'][next_player]['url'].rstrip('/')

        if len(filter(lambda x: x['active'],  board_data[u'players'])) <= 1:
            # no more players
            logger.warning("GAME END - player %s wins" % player_name)
            board_data['the_end'] = True
            board_data['message'] = "Player %s WINS!" % player_name
            BoardState.objects.create(iteration=iteration, board_data=board_data, state_data=state_data)
            return



        logger.warning('Asking player ID=%d [%s] (%s) for bid.' % (player_id, player_name, player_url))

        try:
            user_data = deepcopy(state_data)
            user_data['players'] = [p for p in user_data['players'] if board_data['players'][p['id']]['active']]
            user_data['dice'] = board_data['players'][player_id]['dice']
            user_data['id'] = player_id

            count, die = get_move(player_url + '/bid', {'data': json.dumps(user_data)})
            check_move(count, die, state_data['gameplay'], sum([len(x['dice']) for x in board_data['players'] if x['active']]))

            if count == 0 and die == 0:
                last_player_id, last_player_name, last_count, last_die = state_data['gameplay'][-1]


                # Player calls
                logger.warning("Player ID=%d [%s] (%s) - CALL" % (player_id, player_name, player_url))
                dice_count_list = []
                for player_dice in board_data['players']:
                    dice_count_list += player_dice
                dice_count = len([d for d in dice_count_list if d == last_die])
                if dice_count >= last_count:
                    # User call - success
                    logger.warning("Player %s calls and WIN" % player_name)
                    board_data['message'] = "Player %s calls and WIN" % player_name

                    if len(board_data['players']['last_player_id']['dice']) >= MAX_DICE:
                        # Last player looses
                        board_data['players']['last_player_id']['active'] = False
                    else:
                        # Last player takes one die
                        state_data['players']['last_player_id']['dice'] + 1



                else:
                    # User failed
                    logger.warning("Player %s calls and LOOSE" % player_name)
                    board_data['message'] = "Player %s calls and LOOSE" % player_name

                    if len(board_data['players']['player_id']['dice']) >= MAX_DICE:
                        # Player looses
                        board_data['players']['player_id']['active'] = False
                    else:
                        # Player takes one die
                        state_data['players']['player_id']['dice'] + 1


                board_data['last_player'] = None
                state_data['gameplay'].append(player_id, player_name, last_count, last_die)
                BoardState.objects.create(iteration=iteration, board_data=board_data, state_data=state_data)



            else:
                # Player bids
                board_data['players'][player_id]['bid'] = [count, die]
                state_data['gameplay'].append([player_id, player_name, count, die])
                logger.warning(
                    "Player ID=%d [%s] (%s) - BID - %d, %d" % (player_id, player_name, player_url, count, die))

            board_data['last_player'] = player_id
            BoardState.objects.create(iteration=iteration, board_data=board_data, state_data=state_data)

        except GameError, e:
            # Player errors
            logger.error("Player ID=%d [%s] (%s) - GAME ERROR - %s" % (player_id, player_name, player_url, e))
            requests.get(player_url + '/error', params={'message': str(e)}, timeout=0.5)

            board_data['last_player'] = player_id
            board_data['players'][player_id]['active'] = False
            board_data['message'] = 'Player %s has been disqualified' % player_name
            BoardState.objects.create(iteration=iteration, board_data=board_data, state_data=state_data)


        board_iteration.delay(iteration+1)

    else:
        logger.error("Current iteration %d exists (and should not)" % iteration)
