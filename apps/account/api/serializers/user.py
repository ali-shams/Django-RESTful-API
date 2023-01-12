from rest_framework import serializers

from apps.account.models import User


class UserSerializers(serializers.Serializer):
    username = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    is_verified = serializers.BooleanField()


class UserRegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password", "password2")

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        del validated_data["password2"]
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Password mismatch.')
        return attrs
