from django.contrib.auth.models import User
from django.db import models

from jsonfield import JSONField


class UserProfilesGamersManager(models.Manager):
    def get_queryset(self):
        return super(UserProfilesGamersManager, self).get_queryset().exclude(url__isnull=True).exclude(
            url='').select_related('user')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.URLField(blank=True, null=True, help_text="Provide URL of your gamer service: http://...",
                          max_length=150)

    objects = models.Manager()
    active_gamers = UserProfilesGamersManager()

    def __unicode__(self):
        return u"%s (%s)" % (self.user.username, self.url)


class BoardState(models.Model):
    iteration = models.IntegerField(db_index=True, unique=True)
    board_data = JSONField()
    state_data = JSONField()

    class Meta:
        ordering = ('iteration',)

    def __unicode__(self):
        return u"Iteration %d" % self.iteration

# noinspection PyUnresolvedReferences
import board.signals