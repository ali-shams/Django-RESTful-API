from django.apps import apps
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from rest_framework import (
    status,
    mixins,
)

from apps.account.api.serializers import ListTokensSerializer

UserAgent = apps.get_model("account", "UserAgent")


class ListTokensViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = ListTokensSerializer

    @action(methods=['GET'], detail=False)
    def tokens(self, request):
        queryset = AuthToken.objects.filter(user=request._auth.user).annotate(user_ag=F('user_agent__user_agent'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK
                        )


class KillTokensView(APIView):
    def post(self, request):
        breakpoint()
        # serializer = CreateUserSerializer(data=request.data)
        # user_agent = request.META.get('HTTP_USER_AGENT')
        # is_user_agent_header_exist(user_agent)
