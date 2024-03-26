from rest_framework.response import Response
from rest_framework import status

from apps.utils.base import BaseViewSet


class ArtistViewSet(BaseViewSet):

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
