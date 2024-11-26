from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "user_img",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data["password"]
        validated_data["password"] = make_password(password)  # 비밀번호를 수동으로 해시화
        user = settings.AUTH_USER_MODEL.objects.create(**validated_data)
        return user
