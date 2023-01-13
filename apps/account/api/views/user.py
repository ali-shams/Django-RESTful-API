from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_out
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from knox.models import AuthToken
from knox.auth import TokenAuthentication

from painless.factory import getOTP
from apps.account.api.serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    ChangePassSerializer,
    ForgotPassSerializer,
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
        get_otp_code, phone_number = request.data['otp_code'], request._auth.user.phone_number
        otp_code = cache.get(phone_number)
        if otp_code is None:
            return Response({
                "msg": f"OTP expired, try again."
            }, status=status.HTTP_100_CONTINUE)
        elif otp_code == get_otp_code:
            User.dal.set_user_active(phone_number)
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response({
                "msg": f"OTP mismatch."
            }, status=status.HTTP_100_CONTINUE)


class ChangePassPView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = ChangePassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data.get("old_password")):
            raise ValidationError(_('Your old password was '
                                    'entered incorrectly. Please enter it again.'))

        if serializer.data['new_password'] != serializer.data['new_password_repeat']:
            raise ValidationError(_("The two password fields didn't match."))

        password_validation.validate_password(serializer.data['new_password'], request.user)
        request.user.set_password(serializer.data.get("new_password"))
        request.user.save()
        return Response({
            "token": AuthToken.objects.create(request.user)[1]
        }, status=status.HTTP_200_OK)


class ForgotPassPView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        breakpoint()
        serializer = ForgotPassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        get_otp_code, phone_number = request.data['otp_code'], request.data['phone_number']
        breakpoint()
        otp_code = cache.get(phone_number)
        if otp_code is None:
            return Response({
                "msg": f"OTP expired, Try again."
            }, status=status.HTTP_100_CONTINUE)
        elif otp_code == get_otp_code and \
                serializer.data['new_password'] == serializer.data['new_password_repeat']:
            password_validation.validate_password(serializer.data['new_password'], request.user)
            request.user.set_password(serializer.data.get("new_password"))
            request.user.save()
            return Response({
                "token": AuthToken.objects.create(request.user)[1]
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "msg": f"Password mismatch.."
            }, status=status.HTTP_100_CONTINUE)


class ListTokensView(APIView):
    ...


class KillTokensView(APIView):
    ...
