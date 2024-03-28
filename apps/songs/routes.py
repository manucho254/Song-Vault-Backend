from rest_framework.routers import DefaultRouter

from apps.songs.views import SongViewSet

router = DefaultRouter()

router.register("", SongViewSet, basename="songs")