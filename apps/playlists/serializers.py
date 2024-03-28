from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.playlists.models import Playlist
from apps.songs.serializers import SongSerializer


class PlayListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ["playlist_id", "user", "name", "songs", "updated_at", "created_at"]
