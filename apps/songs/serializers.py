from rest_framework import serializers

from apps.artists.serializers import ArtistSerializer
from apps.songs.models import Song, SongGenre, SongMedia


class SongGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = SongGenre
        fields = ["genre_id", "name", "updated_at", "created_at"]


class SongMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SongMedia
        fields = ["media_id", "image", "file", "updated_at", "created_at"]


class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=False, read_only=True)
    song_media = SongMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = [
            "song_id",
            "title",
            "artist",
            "lyrics",
            "duration",
            "song_media",
            "genre",
            "updated_at",
            "created_at",
        ]
