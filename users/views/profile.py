import pdb

from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from config.settings import SPECTACULAR_SETTINGS
# from common.views.mixins import ListViewSet
# from users.permissions import IsNotCorporate
from users.serializers import profile as user_s

User = get_user_model()


@extend_schema(tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['PROFILE']])
@extend_schema_view(
    get=extend_schema(summary='Профиль пользователя',),
    put=extend_schema(summary='Изменение профиля пользователя',),
    patch=extend_schema(summary='Частичное изменение профиля пользователя',),
)
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = user_s.ProfileListSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return user_s.ProfileUpdateSerializer
        return user_s.ProfileListSerializer

    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(summary='Смена пароля', tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['PROFILE']]),
)
class ChangePasswordView(APIView):
    serializer_class = user_s.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        user = request.user
        serializer = user_s.ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(HTTP_204_NO_CONTENT)