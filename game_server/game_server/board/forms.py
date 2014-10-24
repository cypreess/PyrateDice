from django.forms import ModelForm
from board.models import UserProfile

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['url']
