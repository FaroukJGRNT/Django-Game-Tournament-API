from django.contrib import admin
from .models import Game, Tournament

class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ["name"]

class TournamentAdmin(admin.ModelAdmin):
    list_display = ("name", "game", "start_date", "end_date")
    list_display_links = ["name"]
    list_filter = ["game"]

admin.site.register(Game, GameAdmin)
admin.site.register(Tournament, TournamentAdmin)
# Register your models here.
