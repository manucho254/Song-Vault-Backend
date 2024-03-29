from django.contrib import admin

from apps.songs.models import SongGenre, Song, SongMedia


class SongAdmin(admin.ModelAdmin):
    list_display = [
        "song_id",
        "title",
        "artist",
        "genre",
        "updated_at",
        "created_at",
    ]


class SongGenreAdmin(admin.ModelAdmin):
    list_display = ["genre_id", "name", "updated_at", "created_at"]


class SongMediaAdmin(admin.ModelAdmin):
    list_display = ["media_id", "updated_at", "created_at"]


admin.site.register(Song, SongAdmin)
admin.site.register(SongGenre, SongGenreAdmin)
admin.site.register(SongMedia, SongMediaAdmin)
