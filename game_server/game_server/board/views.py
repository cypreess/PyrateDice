from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import UpdateView
from board.models import UserProfile


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)


@login_required()
def profile(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)

class UserProfileUpdate(UpdateView):
    model = UserProfile
    fields = ['url']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        print self.request.user
        print queryset.filter(user=self.request.user)

        return queryset.filter(user=self.request.user)[0]
