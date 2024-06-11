from apps.accounts.views import (
    RegisterArtistViewSet,
    RegisterUserViewSet,
    LoginViewSet,
    PassWordChangeViewSet,
    PassWordResetViewSet,
    ConfirmEmailViewSet,
    RefreshTokenViewSet,
    userProfileViewSet,
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("register-user", RegisterUserViewSet, basename="Register User")
router.register("register-artist", RegisterArtistViewSet, basename="Register Artist")
router.register("login", LoginViewSet, basename="Login User")
router.register("confirm-email", ConfirmEmailViewSet, basename="Confirm email")
router.register("reset-password", PassWordResetViewSet, basename="Reset password")
router.register("change-password", PassWordChangeViewSet, basename="Change password")
router.register("refresh-token", RefreshTokenViewSet, basename="Refresh token")
router.register("profile", userProfileViewSet, basename="User profile")

