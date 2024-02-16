from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import SPECTACULAR_SETTINGS


User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary='Аутентификация пользователя в системе',
        tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['AUTH']],
        description='Аутентификация пользователя в системе и получение токена',
    ),
)
class LoginView(ObtainAuthToken):
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Выход пользователя из системы',
        tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['AUTH']],
        description='Выход пользователя из системы и удаление токена',
    ),
)
class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    @extend_schema(request=None, responses={200: {"type": "string"}})
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
