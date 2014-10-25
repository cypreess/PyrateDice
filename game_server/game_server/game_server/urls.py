from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from board.views import UserProfileUpdate
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    url(r'^start_game', 'board.views.start_game', name='start_game'),
    url(r'^board', 'board.views.board', name='board'),

    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', login_required(UserProfileUpdate.as_view()), name='profile'),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
)
