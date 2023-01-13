from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from knox.auth import TokenAuthentication

from painless.factory import getOTP
from apps.account.api.serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    # SendOTPSerializer,
)

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "token": AuthToken.objects.create(user)[1]
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        is_sent = cache.get(phone_number)
        if is_sent is None:
            otp_code = getOTP(phone_number)
            cache.set(phone_number, otp_code, timeout=settings.CACHE_TTL)
        else:
            return Response({
                "msg": f"Please try about {cache.ttl(phone_number)} seconds later."
            }, status=status.HTTP_100_CONTINUE)
        return Response(None, status=status.HTTP_200_OK)


class ValidateOTPView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        get_otp_code, phone_number = request.data['otp_code'], request.data['phone_number']
        otp_code = cache.get(phone_number)
        if otp_code is None:
            return Response({
                "msg": f"OTP expired."
            }, status=status.HTTP_100_CONTINUE)
        elif otp_code == get_otp_code:
            User.dal.set_user_active(phone_number)
            return Response(None, status=status.HTTP_200_OK)
