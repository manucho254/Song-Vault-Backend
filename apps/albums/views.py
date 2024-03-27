from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from apps.artists.models import Artist
from apps.songs.models import Song, SongGenre, SongMedia
from apps.utils.base import BaseViewSet
from apps.albums.serializers import AlbumSerializer
from apps.albums.models import Album
from apps.utils.helpers import (
    check_file_size,
    valid_image_extension,
    valid_mp3_extension,
)
from apps.utils.pagination import CustomPagination


class AlbumViewSet(BaseViewSet):
    queryset = Album.objects.all().select_related("artist")
    serializer_class = AlbumSerializer
    pagination_class = CustomPagination()

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        user: User = User.objects.get(user_id=request.user.user_id)
        artist: Artist = Artist.objects.filter(user=user).first()
        serializer = AlbumSerializer(data=data)
        songs = data.get("songs", [])
        song_list = []

        if not artist:
            return Response(
                data={"error": "Forbidden."}, status=status.HTTP_403_FORBIDDEN
            )

        if not serializer.is_valid():
            return Response(
                data={"error": "Invalid data provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for song in songs:
            if check_file_size(song.image) > 2:  # check image file size
                return Response(
                    data={"error": "Song Cover too large."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not valid_image_extension(str(song.image)):  # check image file extension
                return Response(
                    data={"error": "Invalid Song Cover extension."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if check_file_size(song.file) > 10:  # check mp3 file size
                return Response(
                    data={"error": "Mp3 file too large."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not valid_mp3_extension(str(song.file)):  # check mp3 file extension
                return Response(
                    data={"error": "Invalid file extension."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            media = {"image": song.image, "file": song.file}
            del song["image"]
            del song["file"]
            del song["artist"]

            # add song media and song to db
            media_obj, media_created = SongMedia.objects.update_or_create(**media)
            song_obj, song_created = Song.objects.update_or_create(**song)
            song_obj.artist = artist
            song_obj.save()
            media_obj.song = song_obj
            media_obj.save()

            song_list.append(song_obj)

        if check_file_size(data.cover_image) > 2:  # check image file size
            return Response(
                data={"Error": "Album Cover too large."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not valid_image_extension(
            str(data.cover_image)
        ):  # check image file extension
            return Response(
                data={"error": "Invalid Album Cover extension."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        del data["songs"]
        del data["artist"]
        if serializer.is_valid():
            album, created = self.queryset.update_or_create(**data)
            album.artist = artist
            for song in song_list:
                album.songs.append(song)
                album.save()
            album.save()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """Get all albums

        Args:
            request (_type_): request object
        Returns:
            _type_: response object
        """
        paginated_res = self.pagination_class.get_paginated_response(
            query_set=self.queryset,
            serializer_obj=AlbumSerializer,
            request=request,
        )

        return Response(data=paginated_res, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        album_id = kwargs.get("album_id")
        album = self.queryset.filter(album_id=album_id).first()

        if not album:
            return Response(
                data={"error": "Album not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(album)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        album_id = kwargs.get("album_id")
        user: User = User.objects.get(user_id=request.user.user_id)
        artist: Artist = Artist.objects.filter(user=user).first()
        album = self.queryset.filter(album_id=album_id).first()

        if not artist:
            return Response(
                data={"error": "Forbidden."}, status=status.HTTP_403_FORBIDDEN
            )

        if not album:
            return Response(
                data={"error": "Album not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(album)
        return Response(
            data={"message": "Album updated successfully"}, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        album_id = kwargs.get("album_id")
        user: User = User.objects.get(user_id=request.user.user_id)
        artist: Artist = Artist.objects.filter(user=user).first()
        album = self.queryset.filter(album_id=album_id).first()

        return Response(status=status.HTTP_204_NO_CONTENT)
