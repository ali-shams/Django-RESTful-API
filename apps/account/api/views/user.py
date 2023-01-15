from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    UpdateAPIView,
)

from painless.factory import getOTP
from apps.account.api.serializers import (
    CreateUserSerializer,
    LoginUserSerializer,
    SendOTPViewSerializer,
    ValidateOTPSerializer,
    ChangePassSerializer,
    ForgotPassSerializer,
)

User = get_user_model()
UserAgent = apps.get_model("account", "UserAgent")


def is_user_agent_header_exist(user_agent):
    if not user_agent:
        raise ValidationError({
            "user-agent": _('user-agent required.')
        })


class RegisterView(GenericAPIView):
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        user_agent = request.META.get('HTTP_USER_AGENT')
        is_user_agent_header_exist(user_agent)

        request.data._mutable = True
        request.data['phone_number'] = request.data['phone_number'].replace("+98", "0")
        request.data['username'] = request.data['username'].lower()
        request.data._mutable = False

        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        token = AuthToken.objects.create(user)
        UserAgent.dal.save_user_agent(
            user_agnet=user_agent,
            token_id=token[0],
        )
        return Response({
            "token": token[1]
        },
            status=status.HTTP_200_OK
        )


class LoginView(GenericAPIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        user_agent = request.META.get('HTTP_USER_AGENT')
        is_user_agent_header_exist(user_agent)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token = AuthToken.objects.create(user)
        UserAgent.dal.save_user_agent(
            user_agnet=user_agent,
            token_id=token[0],
        )
        return Response({
            "token": token[1]
        },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT')
        is_user_agent_header_exist(user_agent)
        if str(request._auth.user_agent) != user_agent:
            # update user_agent for delete
            user_agent = request._auth.user_agent

        UserAgent.dal.delete_all_user_agent(user_agent)

        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPViewSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number'].replace("+98", "0")
        is_sent = cache.get(phone_number)
        if is_sent is None:
            otp_code = getOTP(phone_number)
            cache.set(phone_number, otp_code, timeout=settings.CACHE_TTL)
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response({
                "msg": f"Please try about {cache.ttl(phone_number)} seconds later."
            },
                status=status.HTTP_100_CONTINUE
            )


class ValidateOTPView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        serializer = ValidateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        get_otp_code = serializer.validated_data['otp_code']
        phone_number = request._auth.user.phone_number
        otp_code = cache.get(phone_number)
        if otp_code is None:
            return Response({
                "msg": "OTP expired, Try again."
            }, status=status.HTTP_100_CONTINUE)
        elif otp_code == get_otp_code:
            User.dal.set_user_verified(phone_number)
            return Response(None, status=status.HTTP_200_OK)
        else:
            return Response({
                "msg": "OTP mismatch."
            }, status=status.HTTP_100_CONTINUE)


class ChangePassPView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = ChangePassSerializer(data=request.data)
        user_agent = request.META.get('HTTP_USER_AGENT')
        is_user_agent_header_exist(user_agent)
        if str(request._auth.user_agent) != user_agent:
            # update user_agent
            UserAgent.dal.update_user_agent(user_agent, request._auth)

        serializer.is_valid(raise_exception=True)
        # breakpoint()
        if not request.user.check_password(serializer.data.get("old_password")):
            raise ValidationError({
                "password": _('Your old password was '
                              'entered incorrectly. Please enter it again.')
            })

        if not request.user.is_verified:
            raise ValidationError({
                "password": _("Please verified first.")
            })

        request.user.set_password(serializer.data.get("new_password"))
        request.user.save()
        AuthToken.objects.filter(user_id=request.user.id).all().delete()
        token = AuthToken.objects.create(request.user)
        UserAgent.dal.save_user_agent(
            user_agnet=user_agent,
            token_id=token[0],
        )
        return Response({
            "token": token[1]
        },
            status=status.HTTP_200_OK
        )


class ForgotPassPView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        serializer = ForgotPassSerializer(data=request.data)
        user_agent = request.META.get('HTTP_USER_AGENT')
        is_user_agent_header_exist(user_agent)

        serializer.is_valid(raise_exception=True)

        get_otp_code = serializer.validated_data['otp_code']
        phone_number = serializer.validated_data['phone_number']

        otp_code = cache.get(phone_number)
        if otp_code is None:
            return Response({
                "msg": f"OTP expired, Try again."
            },
                status=status.HTTP_100_CONTINUE
            )
        elif otp_code == get_otp_code and \
                serializer.data['new_password'] == serializer.data['new_password_repeat']:
            user = User.dal.find_user_by_phone_number(phone_number)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            AuthToken.objects.filter(user_id=user.id).all().delete()
            token = AuthToken.objects.create(user)
            UserAgent.dal.save_user_agent(
                user_agnet=user_agent,
                token_id=token[0],
            )
            return Response({
                "token": token[1]
            },
                status=status.HTTP_200_OK
            )
        elif otp_code != get_otp_code:
            return Response({
                "otp_code": f"Invalid."
            },
                status=status.HTTP_100_CONTINUE
            )

        else:
            return Response({
                "msg": f"Password mismatch."
            }, status=status.HTTP_100_CONTINUE)
