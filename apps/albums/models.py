from uuid import uuid4
from django.db import models

from apps.songs.models import Song
from apps.artists.models import Artist


class Album(models.Model):

    album_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="artist_album",
        blank=True,
    )
    cover_image = models.ImageField(upload_to="album_covers")
    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="songs_in_album")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Album's"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # change file names on save
        new_name = "album_cover_{}.{}".format(
            str(uuid4()), self.cover_image.name.split(".")[-1]
        )
        self.cover_image.name = new_name

        super(Album, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete local files on delete"""
        if self.cover_image:
            self.cover_image.delete()
        return super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.title)
