from django.contrib import admin

# Register your models here.
from board.models import UserProfile, BoardStates


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'url')

admin.site.register(UserProfile, UserProfileAdmin)


class BoardStatesAdmin(admin.ModelAdmin):
    list_display = ('iteration', )
admin.site.register(BoardStates, BoardStatesAdmin)
