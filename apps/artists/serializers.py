from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.artists.models import Artist


class ArtistSerializer(serializers.Serializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Artist
        fields = ["artist_id", "user", "about", "created_at", "updated_at"]
