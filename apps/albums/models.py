from uuid import uuid4
from django.db import models

from apps.songs.models import Song
from apps.artists.models import Artist


class Album(models.Model):

    album_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    artist_album = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artist_album",
        blank=True,
    )
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="songs_in_album")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Album's"
        ordering = ["-created_at"]

    def __str__(self):
        return "{}".format(self.title)
