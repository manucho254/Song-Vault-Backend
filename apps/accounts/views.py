from apps.utils.helpers import decode_token, encode_token
from apps.accounts.serializers import UserSerializer
from apps.accounts.models import User
from apps.utils.base import AuthBaseViewSet

from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError


class RegisterViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, username, password, confirm_password, is_artist = (
            data.get("email"),
            data.get("username"),
            data.get("password"),
            data.get("confirm_password"),
            data.get("is_artist", False),
        )
        if not email or not username or not password or not confirm_password:
            return Response(
                data={"Error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not email:
            return Response(
                data={"Error": "Email required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not username:
            return Response(
                data={"Error": "Username required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"Error": "Password required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not confirm_password:
            return Response(
                data={"Error": "Confirm Password required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != confirm_password:
            return Response(
                data={"Error": "Passwords don't match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8 or len(confirm_password) < 8:
            return Response(
                data={"Error": "Password too short!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(email=email).first()

        # check if account exists
        if user:
            return Response(
                data={"Error": "User account already exists!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(email=email)
        user.username = username
        user.is_artist = is_artist
        user.set_password(str(password))
        user.save()

        token = encode_token({"user_id": user.id}, 24)  # expire in 24 hours
        # send email later
        # send_email()

        return Response(
            data={"Message": "Account created successfully."},
            status=status.HTTP_201_CREATED,
        )


class LoginViewSet(AuthBaseViewSet, TokenObtainPairSerializer):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, password = data.get("email"), data.get("password")

        if not email or not password:
            return Response(
                data={"Error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not email:
            return Response(
                data={"Error": "Email required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"Error": "Password required"}, status=status.HTTP_400_BAD_REQUEST
            )

        auth = authenticate(request=request, email=email, password=password)

        if not auth:
            return Response(
                data={"Error": "Invalid credentials provided!"},
                status=status.HTTP_404_NOT_FOUND,
            )

        tokens = self.get_token(auth)
        auth_data = {
            "access_token": str(tokens.access_token),
            "refresh": str(tokens),
        }

        return Response(auth_data, status=status.HTTP_200_OK)


class ConfirmEmailViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email, token = data.get("email"), data.get("token")

        if not email or not token:
            return Response(
                data={"Error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not email:
            return Response(
                data={"Error": "Email required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not token:
            return Response(
                data={"Error": "Token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        token = decode_token(token)
        if not token:
            Response(
                data={"Error": "Token invalid or expired, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=token.get("user_id"))
        user.email_verified = True
        user.save()

        return Response(
            data={"Message": "Email Sent successfully"}, status=status.HTTP_200_OK
        )


class PassWordResetViewSet(AuthBaseViewSet):

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        email = data.get("email")

        if not email:
            return Response(
                data={"Error": "Email required"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                data={"Error": "User not found!"}, status=status.HTTP_404_NOT_FOUND
            )

        user_serializer = UserSerializer(user)
        token = encode_token({"user_id": user_serializer.id})

        # send_email(token)

        return Response(
            data={"Message": "Email Sent successfully"}, status=status.HTTP_200_OK
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
                data={"Error": "Invalid data provided!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not token:
            return Response(
                data={"Error": "Token required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                data={"Error": "Password required!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not confirm_password:
            return Response(
                data={"Error": "Confirm Password required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if password != confirm_password:
            return Response(
                data={"Error": "Passwords don't match!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(password) < 8 or len(confirm_password) < 8:
            return Response(
                data={"Error": "Password too short!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token = decode_token(token)
        if not token:
            Response(
                data={"Error": "Token invalid or expired, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(id=token.get("user_id"))
        user.set_password(str(password))
        user.save()

        return Response(
            data={"Message": "Password Changed Successfully."},
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
