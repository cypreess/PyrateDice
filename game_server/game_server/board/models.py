from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfilesGamersManager(models.Manager):
    def get_queryset(self):
        return super(UserProfilesGamersManager, self).get_queryset().exclude(url__isnull=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    url = models.URLField(blank=True, null=True, help_text="Provide http url of your machine")
    active_gamers=UserProfilesGamersManager()

# noinspection PyUnresolvedReferences
import board.signals