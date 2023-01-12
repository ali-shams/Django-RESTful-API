from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password", "password2")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Password mismatch.")
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)
