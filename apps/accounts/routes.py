from apps.accounts.views import (
    RegisterArtistViewSet,
    RegisterUserViewSet,
    LoginViewSet,
    PassWordChangeViewSet,
    PassWordResetViewSet,
    ConfirmEmailViewSet,
    RefreshTokenViewSet,
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("register-user", RegisterUserViewSet, basename="Register User")
router.register("register-artist", RegisterArtistViewSet, basename="Register Artist")
router.register("login", LoginViewSet, basename="Login User")
router.register("confirm_email", ConfirmEmailViewSet, basename="Confirm email")
router.register("reset_password", PassWordResetViewSet, basename="Reset password")
router.register("change_password", PassWordChangeViewSet, basename="Change password")
router.register("refresh_token", RefreshTokenViewSet, basename="Refresh token")
