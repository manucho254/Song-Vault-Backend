from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from apps.songs.models import Song
from apps.utils.base import BaseViewSet
from apps.playlists.models import Playlist
from apps.playlists.serializers import PlayListSerializer
from apps.utils.pagination import CustomPagination


class PlayListViewSet(BaseViewSet):

    queryset = Playlist.objects.all()
    serializer_class = PlayListSerializer
    pagination_class = CustomPagination()

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        user: User = User.objects.get(request.user.user_id)
        serializer = self.serializer_class(data=data)
        songs = data.get("songs", [])

        if not serializer.is_valid():
            return Response(
                data={"error": "Invalid data provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        del data["songs"]
        del data["user"]
        playlist, created = self.queryset.update_or_create(**data)
        playlist.user = user
        for song_id in songs:
            obj = Song.objects.filter(song_id=song_id).first()
            playlist.songs.append(obj)
            playlist.save()
        playlist.save()

        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        paginated_res = self.pagination_class.get_paginated_response(
            query_set=self.queryset,
            serializer_obj=self.serializer_class,
            request=request,
        )
        return Response(data=paginated_res, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        playlist_id = kwargs.get("playlist_id")
        playlist = self.queryset.filter(playlist_id=playlist_id).first()

        if not playlist:
            return Response(
                data={"error": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(playlist)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data: dict = request.data
        playlist_id = kwargs.get("playlist_id")
        user = User.objects.get(user_id=request.user.user_id)
        playlist = self.queryset.filter(user=user, playlist_id=playlist_id).first()

        if not playlist:
            return Response(
                data={"error": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(playlist, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                data={"error": "Invalid data provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
