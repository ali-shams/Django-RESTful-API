from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password", "password2")

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(_("Password mismatch."))
        return attrs


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(_("Invalid Details."))


class ChangePassSerializer(serializers.Serializer):
    restrict = {
        'max_length': 128,
        'required': True
    }
    old_password = serializers.CharField(**restrict)
    new_password = serializers.CharField(**restrict)
    new_password_repeat = serializers.CharField(**restrict)


class ForgotPassSerializer(serializers.Serializer):
    restrict = {
        'max_length': 128,
        'required': True
    }
    phone_number = serializers.CharField(required=True)
    otp_code = serializers.CharField(required=True)
    new_password = serializers.CharField(**restrict)
    new_password_repeat = serializers.CharField(**restrict)
