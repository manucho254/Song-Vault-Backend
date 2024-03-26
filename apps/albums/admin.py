from django.contrib import admin
from apps.albums.models import Album


class AlbumAdmin(admin.ModelAdmin):
    list_display = ["album_id", "artist", "title", "created_at", "updated_at"]


admin.site.register(Album, AlbumAdmin)
