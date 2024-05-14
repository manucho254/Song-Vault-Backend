""" Urls module
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.accounts import routes as account_routes
from apps.albums import routes as album_routes
from apps.artists import routes as artist_routes
from apps.playlists import routes as playlist_routes
from apps.songs import routes as song_routes
from apps.core import routes as core_routes

schema_view = get_schema_view(
    openapi.Info(
        title="Song Vault API",
        default_version="v1",
        description="Song Vault API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="manuchoadero@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include(account_routes.router.urls)),
    path("api/albums/", include(album_routes.router.urls)),
    path("api/artists/", include(artist_routes.router.urls)),
    path("api/playlists/", include(playlist_routes.router.urls)),
    path("api/songs/", include(song_routes.router.urls)),
    path("api/search/", include(core_routes.router.urls)),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
