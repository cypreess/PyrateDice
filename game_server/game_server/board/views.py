from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render_to_response
from django.views.generic import UpdateView
import requests
from board.models import UserProfile, BoardStates


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


@login_required()
def start_game(request, *args, **kwargs):
    if not request.user.is_superuser:
        return HttpResponse('You should be admin to display this page')

    BoardStates.delete()

    empty_board_state = {
        "results": {
            "new_die": "",
            "player_lose": "",
            "player_win": "",
        },
        "board": []
    }

    gamers = []
    for user in UserProfile.active_gamers.all():
        gamers.append({
            "name": user.user_name,
            "avatar" : "",
            "dice": [],
            "bid": [],
            "current": False,
            "active": True,
        })

    gamers.shuffle()

    #
    # {
    # "results" : {
    # "new_die" : "player_name", # ""
    # 		"player_lose" : "player_name", # or ""
    # 		"player_win": "player_name", # ""
    # 	},
    # 	"board" : [
    # 		{
    # 			id: 1,
    # 			name: "cypreess",
    # 			avatar: http://...,
    # 			dice: [1,2,3,4],
    # 			bid: [2, 5],  #  [] == CHECK
    # 			current: ture #
    # 			active: true #
    # 		},
    #
    # 		{
    # 		... user 2 ...
    # 		}
    #
    # 	]
    # }

    BoardStates.objects.create(iteration=0)
    return HttpResponse('Start new')


@login_required()
def board(request, *args, **kwargs):
    return render_to_response('board/board.html')


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

