import json
from random import shuffle, randrange

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse


# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import UpdateView, DetailView
import requests
from board.models import UserProfile, BoardState
from board.tasks import board_iteration


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


@login_required()
def start_game(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponse('You should be admin to display this page')

    BoardState.objects.all().delete()

    empty_board_state = {
        "the_end": False,
        "message": "",
        "last_player": None,
        "players": []
    }

    players = []
    for user_profile in UserProfile.active_gamers.all():
        players.append({
            "name": user_profile.user.username,
            "url": user_profile.url,
            "avatar": "",
            "dice": [],
            "bid": [],
            "active": True,
        })

    shuffle(players)
    for i, gamer in enumerate(players):
        gamer['id'] = i
    empty_board_state['players'] = players

    empy_state_data = {
        'gameplay': [],
        'players': []
    }
    for user in players:
        empy_state_data['players'].append({'id': user['id'], 'name': user['name'], 'dice': 1})

    BoardState.objects.create(iteration=0, board_data=empty_board_state, state_data=empy_state_data)
    board_iteration.delay(iteration=1)
    return HttpResponse('Start new')


@login_required()
def board(request, *args, **kwargs):
    return render_to_response('board/board.html')


# @login_required()
def board_json(request, pk):
    object = get_object_or_404(BoardState.objects.filter(iteration=pk))
    return HttpResponse(json.dumps(object.board_data))



class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['url']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return queryset.filter(user=self.request.user)[0]

    def form_valid(self, form):
        url = form.cleaned_data['url']
        url = url.rstrip('/')
        try:
            r = requests.get(url + '/ping', timeout=1)
        except:
            messages.add_message(self.request, messages.ERROR,
                                 'Your URL does not reply "pong" on %s/ping [HTTP %d]' % (url, r.status_code))
            return self.form_invalid(form)

        if r.status_code == 200 and r.text.strip() == 'pong':
            messages.add_message(self.request, messages.SUCCESS,
                                 'Ping-Pong OK! URL successfully saved!')
            return super(UserProfileUpdate, self).form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR,
                                 'Your URL does not reply "pong" on %s/ping [HTTP %d]' % (url, r.status_code))
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('profile')

