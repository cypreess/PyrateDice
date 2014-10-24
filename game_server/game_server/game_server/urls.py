from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from board.views import UserProfileUpdate

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'game_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^start_game', 'board.views.start_game', name='start_game'),
    url(r'^board', 'board.views.board', name='board'),

    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', login_required(UserProfileUpdate.as_view()), name='profile'),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
)
