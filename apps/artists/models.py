from uuid import uuid4

from django.db import models

from apps.accounts.models import User


class Artist(models.Model):

    artist_id = models.UUIDField(max_length=255, default=uuid4, primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="artist_user"
    )
    about = models.TextField(max_length=2000, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Artist's"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return "{} {}".format(self.artist_id, self.user.username)
