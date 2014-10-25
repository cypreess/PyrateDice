from django.contrib import admin

# Register your models here.
from board.models import UserProfile, BoardState


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'url')

admin.site.register(UserProfile, UserProfileAdmin)


class BoardStateAdmin(admin.ModelAdmin):
    list_display = ('iteration', )
admin.site.register(BoardState, BoardStateAdmin)
