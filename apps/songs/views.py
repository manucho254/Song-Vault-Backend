from rest_framework.response import Response
from rest_framework import status

from apps.songs.models import Song, SongMedia
from apps.songs.serializers import SongSerializer
from apps.accounts.models import User
from apps.artists.models import Artist
from apps.utils.helpers import (
    check_file_size,
    valid_image_extension,
    valid_mp3_extension,
)
from apps.utils.pagination import CustomPagination
from apps.utils.base import BaseViewSet


class SongViewSet(BaseViewSet):
    lookup_field = "song_id"
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = CustomPagination()

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        user: User = User.objects.get(id=request.user.id)
        artist: Artist = Artist.objects.filter(user=user).first()
        serializer = self.serializer_class(data=data)

        if not artist:
            return Response(
                data={"Error": "Forbidden."}, status=status.HTTP_403_FORBIDDEN
            )

        if not serializer.is_valid():
            return Response(
                data={"error": "Invalid data provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if check_file_size(data.image) > 2:  # check image file size
            return Response(
                data={"Error": "Song Cover too large."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not valid_image_extension(str(data.image)):  # check image file extension
            return Response(
                data={"Error": "Invalid Song Cover extension."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if check_file_size(data.file) > 10:  # check mp3 file size
            return Response(
                data={"Error": "Mp3 file too large."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not valid_mp3_extension(str(data.file)):  # check mp3 file extension
            return Response(
                data={"Error": "Invalid file extension."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        media = {"image": data.image, "file": data.file}
        del data["image"]
        del data["file"]
        del data["artist"]

        # add song media and song to db
        media_obj, media_created = SongMedia.objects.update_or_create(**media)
        song_obj, song_created = Song.objects.update_or_create(**data)
        song_obj.artist = artist
        song_obj.save()
        media_obj.song = song_obj
        media_obj.save()

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):

        paginated_res = self.pagination_class.get_paginated_response(
            query_set=self.queryset,
            serializer_obj=self.serializer_class,
            request=request,
        )
        return Response(data=paginated_res, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        song_id = kwargs.get("song_id")
        song: Song = self.queryset.filter(song_id=song_id).first()
        serializer = self.serializer_class(song)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        song_id = kwargs.get("song_id")
        user: User = User.objects.get(id=request.user.id)
        artist: Artist = Artist.objects.filter(user=user).first()
        song: Song = self.queryset.filter(song_id=song_id, artist=artist).first()

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        song_id = kwargs.get("song_id")
        user: User = User.objects.get(id=request.user.id)
        artist: Artist = Artist.objects.filter(user=user).first()
        song: Song = self.queryset.filter(song_id=song_id, artist=artist).first()

        return Response(status=status.HTTP_204_NO_CONTENT)
