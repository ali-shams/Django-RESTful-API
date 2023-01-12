from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

from apps.account.models import User
from apps.account.api.serializers import (
    UserSerializers,
    UserRegisterSerializers,
)


class UserAPIView(APIView):
    def get(self, request):
        return Response({"name": "ali"})


class HomeAPIView(APIView):
    def get(self, request):
        users = User.dal.all()
        ser_data = UserSerializers(instance=users, many=True)
        response = Response(data=ser_data.data,
                            status=status.HTTP_200_OK)
        return response


class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            response = Response(data=serializer.data,
                                status=status.HTTP_201_CREATED)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExampleAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {
            'foo': 'bar'
        }
        return Response(content)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
