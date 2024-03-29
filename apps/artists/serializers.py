from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.artists.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Artist
        fields = ["artist_id", "name", "user", "about", "updated_at", "created_at"]
