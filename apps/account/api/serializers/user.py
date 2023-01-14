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
        return User.dal.create_user(**validated_data)

    # def validate_username(self, value):
    #     # breakpoint()
    #     if User.dal.filter(username=value.lower()).exists():
    #         # raise serializers.ValidationError(_("A user with that username already exists."))
    #         # breakpoint()
    #         raise UniqueApiException("username")
    #     return value
    #
    # def validate_phone_number(self, value):
    #     breakpoint()
    #     if User.dal.filter(phone_number=value.replace("+98", "09")).exists():
    #         # raise serializers.ValidationError(_("A user with that username already exists."))
    #         # breakpoint()
    #         raise UniqueApiException("phone_number")
    #     return value

    def validate(self, attrs):
        # breakpoint()
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(_("Password mismatch."))
        return attrs


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
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
