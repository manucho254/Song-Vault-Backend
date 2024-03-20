from rest_framework import serializers

from apps.albums.models import Album
from apps.artists.serializers import ArtistSerializer
from apps.songs.serializers import SongSerializer


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=False, read_only=True)
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ["album_id", "artist", "title", "songs", "updated_at", "created_at"]
