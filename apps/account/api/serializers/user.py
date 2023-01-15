import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoSideValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)

from painless.helper.enums import RegexPatternEnum

User = get_user_model()

restrict = {
    'max_length': 128,
    'required': True
}


def common_password(value):
    try:
        password_validation.validate_password(value)
    except DjangoSideValidationError as e:
        raise serializers.ValidationError(_(e.messages[0]))


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password", "password2")
        extra_kwargs = {
            "password": {"validators": (common_password,)}
        }

    def create(self, validated_data):
        del validated_data["password2"]
        return User.dal.create_user(**validated_data)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({
                "password": _("Password mismatch.")
            })
        return attrs


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError({
            "inputs": _("Invalid.")
        })


class SendOTPViewSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, data):
        RegexValidator(RegexPatternEnum.Iran_phone_number.value)(data)
        MinLengthValidator(11)(data)
        MaxLengthValidator(13)(data)
        return data


class ValidateOTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField()


class ChangePassSerializer(serializers.Serializer):
    old_password = serializers.CharField(**restrict)
    new_password = serializers.CharField(**restrict)
    new_password_repeat = serializers.CharField(**restrict)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_repeat']:
            raise serializers.ValidationError({
                "password": _("Password mismatch.")
            })
        common_password(attrs['new_password'])
        return attrs


class ForgotPassSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    new_password = serializers.CharField(**restrict)
    new_password_repeat = serializers.CharField(**restrict)
    phone_number = serializers.CharField()

    def validate_phone_number(self, data):
        RegexValidator(RegexPatternEnum.Iran_phone_number.value)(data)
        MinLengthValidator(11)(data)
        MaxLengthValidator(13)(data)
        return data

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_repeat']:
            raise serializers.ValidationError({
                "password": _("Password mismatch.")
            })
        common_password(attrs['new_password'])
        return attrs
