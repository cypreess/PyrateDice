from __future__ import absolute_import
import json

from celery import shared_task
from celery.utils.log import get_task_logger
import requests
from requests.exceptions import ReadTimeout

from board.models import BoardState

logger = get_task_logger(__name__)


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


def check_move(count, die, gameplay):
    if not ((count == 0 and die == 0) or (count > 0 and die >= 1 and die <= 6)):
        raise GameError('Bid must be (0, 0) or ( >0 , 1..6 )')
    if count == 0 and die == 0 and len(gameplay) == 0:
        raise GameError('Cannot call as the first player')

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

        print board_data
        print state_data

        board_data[u'message'] = ""
        if board_data[u'last_player'] is None:
            next_player = 0
        else:
            next_player = board_data[u'last_player'] + 1
            if next_player >= len(board_data[u'players']):
                next_player = 0




        player_id = next_player
        player_name = board_data[u'players'][next_player]['name']
        player_url = board_data[u'players'][next_player]['url'].rstrip('/')

        logger.warning('Asking player ID=%d [%s] (%s) for move.' % (player_id, player_name, player_url))

        try:
            count, die = get_move(player_url + '/bid', {'data': json.dumps(state_data)})
            check_move(count, die, state_data['gameplay'])

            if count == 0 and die == 0:
                logger.warning("Player ID=%d [%s] (%s) - CALL" % (player_id, player_name, player_url))
            else:
                board_data['players'][player_id]['bid'] = [count, die]
                state_data['gameplay'].append([player_id, player_name, count, die])
                logger.warning(
                    "Player ID=%d [%s] (%s) - BID - %d, %d" % (player_id, player_name, player_url, count, die))


            BoardState.objects.create(iteration=iteration, board_data=board_data, state_data=state_data)

        except GameError, e:
            logger.error("Player ID=%d [%s] (%s) - GAME ERROR - %s" % (player_id, player_name, player_url, e))
            requests.get(player_url + '/error', params={'message': str(e)}, timeout=0.5)



    else:
        logger.error("Current iteration %d exists (and should not)." % iteration)
