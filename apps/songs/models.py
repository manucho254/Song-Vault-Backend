from uuid import uuid4

from django.db import models

from apps.artists.models import Artist
from apps.utils.helpers import get_genres


class Song(models.Model):

    id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="song_artist"
    )
    lyrics = models.TextField(max_length=2000, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Songs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "Song {} by {}".format(self.name, self.artist.name)


class SongGenre(models.Model):

    category_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    name = models.CharField(max_length=255, choices=get_genres)
    songs = models.ManyToManyField(Song, related_name="songs_genre")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Song Genre's"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "Song Genre {}".format(self.name)


class SongMedia(models.Model):

    media_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    song_media = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artist_media",
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
