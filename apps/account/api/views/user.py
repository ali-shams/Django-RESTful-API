from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from knox.models import AuthToken

from apps.account.api.serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
)


class UserRegisterAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)


class UserLoginAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)
