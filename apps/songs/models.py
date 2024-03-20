from uuid import uuid4

from django.db import models

from apps.artists.models import Artist
from apps.utils.helpers import get_genres


class SongGenre(models.Model):

    genre_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    name = models.CharField(max_length=255, choices=get_genres)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Song Genre's"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "Song Genre {}".format(self.name)


class Song(models.Model):

    id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="song_artist"
    )
    lyrics = models.TextField(max_length=2000, blank=True, null=True)
    genre = models.ForeignKey(
        SongGenre, on_delete=models.CASCADE, related_name="song_genre", null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Songs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "Song {} by {}".format(self.name, self.artist.name)


class SongMedia(models.Model):

    media_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="song_media",
        blank=True,
    )
    image = models.ImageField(upload_to="song_media")
    file = models.FileField(upload_to="music_folder")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Song's Media"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "{}".format(self.media_id)
