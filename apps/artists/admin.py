from django.contrib import admin

from apps.artists.models import Artist


class ArtistAdmin(admin.ModelAdmin):
    list_display = ["artist_id", "user", "created_at", "updated_at"]


admin.site.register(Artist, ArtistAdmin)
