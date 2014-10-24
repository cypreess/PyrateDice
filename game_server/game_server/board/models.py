from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from jsonfield import JSONField


class UserProfilesGamersManager(models.Manager):
    def get_queryset(self):
        return super(UserProfilesGamersManager, self).get_queryset().exclude(url__isnull=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.URLField(blank=True, null=True, help_text="Provide http url of your machine")
    active_gamers = UserProfilesGamersManager()

class BoardStates(models.Model):
    iteration = models.IntegerField(db_index=True)
    data = JSONField()


# noinspection PyUnresolvedReferences
import board.signals