from django.contrib.auth.models import User
from django.db.models.signals import post_save
from board.models import UserProfile


def create_user_profile(sender, instance, created, **kwargs):
    if created and not UserProfile.objects.filter(user=instance).exists():
        print "USER CREATED"
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User, dispatch_uid="create_user_profile")
