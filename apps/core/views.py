from rest_framework import status
from rest_framework.response import Response

from apps.albums.models import Album
from apps.albums.serializers import AlbumSerializer
from apps.artists.models import Artist
from apps.artists.serializers import ArtistSerializer
from apps.songs.models import Song
from apps.songs.serializers import SongSerializer
from apps.utils.base import BaseViewSet


class SearchViewSet(BaseViewSet):

    def list(self, request, *args, **kwargs):
        query = str(request.GET.get("query", ""))
        data = {"songs": [], "albums": [], "artists": []}
        albums = Album.objects.all()
        songs = Song.objects.all()
        artists = Artist.objects.all()

        if not query or query == "":
            data["songs"] = SongSerializer(songs, many=True).data
            data["albums"] = AlbumSerializer(albums, many=True).data
            data["artists"] = ArtistSerializer(artists, many=True).data

            return Response(data, status=status.HTTP_200_OK)

        songs = songs.filter(title__icontains=query)
        artists = artists.filter(name__icontains=query)
        albums = albums.filter(title__icontains=query)

        data["songs"] = SongSerializer(songs, many=True).data
        data["albums"] = AlbumSerializer(albums, many=True).data
        data["artists"] = ArtistSerializer(artists, many=True).data

        return Response(data, status=status.HTTP_200_OK)