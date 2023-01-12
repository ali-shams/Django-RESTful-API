from rest_framework import serializers


class UserSerializers(serializers.Serializer):
    username = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    is_verified = serializers.BooleanField()
