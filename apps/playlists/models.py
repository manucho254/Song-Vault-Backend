from uuid import uuid4

from django.db import models

from apps.accounts.models import User
from apps.songs.models import Song


class Playlist(models.Model):
    """playlist model
    Args:
        models (_type_): _description_
    """

    playlist_id = models.UUIDField(max_length=255, default=uuid4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playlist_user"
    )
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlist_songs")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Playlists"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "{} {}".format(self.playlist_id, self.name)
