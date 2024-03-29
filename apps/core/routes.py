from rest_framework.routers import DefaultRouter

from apps.core.views import SearchViewSet

router = DefaultRouter()

router.register("", SearchViewSet, basename="search")
