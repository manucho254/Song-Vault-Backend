from apps.artists.models import Artist
from apps.artists.serializers import ArtistSerializer
from apps.utils.helpers import decode_token, encode_token
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User
from apps.utils.base import AuthBaseViewSet, BaseViewSet

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError

from apps.utils.pagination import CustomPagination


class RegisterUserViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, username, password, confirm_password = (
            data.get("email"),
            data.get("username"),
            data.get("password"),
            data.get("confirm_password"),
        )
        if not email or not username or not password or not confirm_password:
            return Response(
                data={"error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email:
            return Response(
                data={"error": "Email required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not username:
            return Response(
                data={"error": "Username required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"error": "Password required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not confirm_password:
            return Response(
                data={"error": "Confirm Password required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirm_password:
            return Response(
                data={"error": "Passwords don't match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8 or len(confirm_password) < 8:
            return Response(
                data={"error": "Password too short!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        # check if account exists
        if user:
            return Response(
                data={"error": "User account already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(email=email, username=username)
        user.set_password(str(password))
        user.save()

        token = encode_token({"user_id": str(user.id)}, 24)  # expire in 24 hours
        # send email later
        # send_email()

        return Response(
            data={"message": "Account created successfully."},
            status=status.HTTP_201_CREATED,
        )


class RegisterArtistViewSet(AuthBaseViewSet):
    queryset = Artist.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination()

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, username, password, confirm_password = (
            data.get("email"),
            data.get("username"),
            data.get("password"),
            data.get("confirm_password"),
        )
        if not email or not username or not password or not confirm_password:
            return Response(
                data={"error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email:
            return Response(
                data={"error": "Email required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not username:
            return Response(
                data={"error": "Username required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"error": "Password required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not confirm_password:
            return Response(
                data={"error": "Confirm Password required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirm_password:
            return Response(
                data={"error": "Passwords don't match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8 or len(confirm_password) < 8:
            return Response(
                data={"error": "Password too short!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        # check if account exists
        if user:
            return Response(
                data={"error": "Artist account already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # save artist
        del data["password"]
        del data["confirm_password"]
        data["is_artist"] = True
        user = User.objects.create(**data)
        user.set_password(str(password))
        user.save()
        artist = self.queryset.create(user=user)
        artist.save()

        token = encode_token({"user_id": str(user.id)}, 24)  # expire in 24 hours
        # send email later
        # send_email()

        return Response(
            data={"message": "Artist account created successfully."},
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(AuthBaseViewSet, TokenObtainPairSerializer):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, password = data.get("email"), data.get("password")

        if not email or not password:
            return Response(
                data={"error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not email:
            return Response(
                data={"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"error": "Password required"}, status=status.HTTP_400_BAD_REQUEST
            )

        auth = authenticate(request=request, email=email, password=password)

        if not auth:
            return Response(
                data={"error": "Invalid credentials provided!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        tokens = self.get_token(auth)
        res_data = UserSerializer(auth).data
        # get artist
        if auth.is_artist:
            auth = Artist.objects.filter(user=auth).first()
            res_data = ArtistSerializer(auth).data

        auth_data = {
            "tokens": {
                "access_token": str(tokens.access_token),
                "refresh": str(tokens),
            },
            "user": res_data,
        }

        return Response(auth_data, status=status.HTTP_200_OK)


class ConfirmEmailViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, token = data.get("email"), data.get("token")

        if not email or not token:
            return Response(
                data={"error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not email:
            return Response(
                data={"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not token:
            return Response(
                data={"error": "Token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        token = decode_token(token)
        if not token:
            Response(
                data={"error": "Token invalid or expired, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=token.get("user_id"))
        user.email_verified = True
        user.save()

        return Response(
            data={"message": "Email Sent successfully"}, status=status.HTTP_200_OK
        )


class PassWordResetViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email = data.get("email")

        if not email:
            return Response(
                data={"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                data={"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        user_serializer = UserSerializer(user)
        token = encode_token({"user_id": str(user_serializer.id)})

        # send_email(token)

        return Response(
            data={"message": "Email Sent successfully"}, status=status.HTTP_200_OK
        )


class PassWordChangeViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        token, password, confirm_password = (
            data.get("token"),
            data.get("password"),
            data.get("confirm_password"),
        )

        if not token or not password or not confirm_password:
            return Response(
                data={"error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not token:
            return Response(
                data={"error": "Token required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"error": "Password required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not confirm_password:
            return Response(
                data={"error": "Confirm Password required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if password != confirm_password:
            return Response(
                data={"error": "Passwords don't match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(password) < 8 or len(confirm_password) < 8:
            return Response(
                data={"error": "Password too short!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = decode_token(token)
        if not token:
            Response(
                data={"error": "Token invalid or expired, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=token.get("user_id"))
        user.set_password(str(password))
        user.save()

        return Response(
            data={"message": "Password Changed Successfully."},
            status=status.HTTP_200_OK,
        )


class RefreshTokenViewSet(AuthBaseViewSet, TokenRefreshView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response(
                {"message": "Token invalid or expired, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class userProfileViewSet(BaseViewSet):
    lookup_field = "user_id"

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(id=request.user.id)

        if not user:
            return Response(
                data={"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
            
        to_update = {
            "username": data.get("username"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "country": data.get("country"),
            "gender": data.get("gender"),
        }

        for key, val in to_update.items():
            setattr(user, key, val)
            user.save()

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
