from rest_framework import serializers

from apps.accounts.models import User, UserMedia


class UserMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMedia
        fields = ["media_id", "image", "updated_at", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    user_media = UserMediaSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "gender",
            "user_media",
            "email_verified",
            "is_artist",
            "is_active",
            "created_at",
            "updated_at",
        ]
