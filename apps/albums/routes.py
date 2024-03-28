from rest_framework.routers import DefaultRouter

from apps.albums.views import AlbumViewSet


router = DefaultRouter()

router.register("", AlbumViewSet, basename="albums")
