import pdb

from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from config.settings import SPECTACULAR_SETTINGS
# from common.views.mixins import ListViewSet
# from users.permissions import IsNotCorporate
from users.serializers import user as user_s

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary='Аутентификация пользователя в системе',
        tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['ADMIN']],
        description='Аутентификация пользователя в системе и получение токена',
    ),
)
class LoginView(ObtainAuthToken):
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Выход пользователя из системы',
        tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['ADMIN']],
        description='Выход пользователя из системы и удаление токена',
    ),
)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema_view(
    post=extend_schema(
        summary='Регистрация пользователя',
        tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['ADMIN']],
        description='Регистрация и создание нового пользователя с пользовательскими правами',
    ),
)
class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = user_s.RegistrationSerializer
