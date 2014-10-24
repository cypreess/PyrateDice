from django.conf.urls import patterns, include, url
from django.contrib import admin
from board.views import UserProfileUpdate

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'game_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^secret$', 'board.views.secret_page', name='secret'),

    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/profile', UserProfileUpdate.as_view(), name='profile'),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
)
