from rest_framework.routers import DefaultRouter

from apps.playlists.views import PlayListViewSet

router = DefaultRouter()


router.register("", PlayListViewSet, basename="playlists")