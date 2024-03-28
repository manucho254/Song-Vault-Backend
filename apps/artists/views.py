from rest_framework.response import Response
from rest_framework import status

from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from apps.artists.models import Artist
from apps.artists.serializers import ArtistSerializer
from apps.utils.base import BaseViewSet
from apps.utils.pagination import CustomPagination


class ArtistViewSet(BaseViewSet):
    lookup_field = "artist_id"
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = CustomPagination()

    def list(self, request, *args, **kwargs):

        paginated_res = self.pagination_class.get_paginated_response(
            query_set=self.queryset,
            serializer_obj=self.serializer_class,
            request=request,
        )
        return Response(data=paginated_res, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        artist_id = kwargs.get("artist_id")
        artist: Artist = Artist.objects.filter(artist_id=artist_id).first()

        if not artist:
            return Response(
                data={"error": "Artist not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        artist_id = kwargs.get("artist_id")
        user: User = User.objects.get(id=request.user.id)
        artist: Artist = Artist.objects.filter(artist_id=artist_id, user=user).first()

        if not artist:
            return Response(
                data={"error": "Artist not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        artist_id = kwargs.get("artist_id")
        user: User = User.objects.get(id=request.user.id)
        artist: Artist = Artist.objects.filter(artist_id=artist_id, user=user).first()

        if not artist:
            return Response(
                data={"error": "Artist not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
