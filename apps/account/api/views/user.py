from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from rest_framework import generics

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from apps.account.api.serializers import CreateUserSerializer


class UserRegisterAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
