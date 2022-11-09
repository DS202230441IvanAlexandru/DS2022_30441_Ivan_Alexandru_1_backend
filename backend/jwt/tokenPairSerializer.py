from abc import ABC

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = "ADMIN" if user.is_superuser else "USER"

        return token


class TokenSerializerView(TokenObtainPairView):
    serializer_class = TokenSerializer
