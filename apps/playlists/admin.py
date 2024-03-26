from django.contrib import admin

from apps.playlists.models import Playlist


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["playlist_id", "user", "name", "updated_at", "created_at"]


admin.site.register(Playlist, PlaylistAdmin)
