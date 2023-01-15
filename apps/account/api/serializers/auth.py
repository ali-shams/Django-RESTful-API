from rest_framework import serializers
from knox.models import AuthToken


class ListTokensSerializer(serializers.HyperlinkedModelSerializer):
    user_ag = serializers.CharField()

    class Meta:
        model = AuthToken
        fields = (
            'token_key',
            'expiry',
            'user_ag'
        )
