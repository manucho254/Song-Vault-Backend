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

    song_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="song_artist"
    )
    lyrics = models.TextField(max_length=2000, blank=True, null=True)
    genre = models.ForeignKey(
        SongGenre, on_delete=models.CASCADE, related_name="song_genre", null=True
    )
    duration = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Songs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "Song {} by {}".format(self.name, self.artist.user.username)


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

    def save(self, *args, **kwargs):
        # change file names on save
        image_name = "song_image_{}.{}".format(
            str(uuid4()), self.image.name.split(".")[-1]
        )
        file_name = "song_mp3_{}.{}".format(str(uuid4()), self.file.name.split(".")[-1])
        self.image.name = image_name
        self.file.name = file_name

        super(SongMedia, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete local files on delete"""
        if self.image:
            self.file.delete()
        if self.file:
            self.file.delete()
        return super(SongMedia, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return "{}".format(self.media_id)
