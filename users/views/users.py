import os.path

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from config.settings import SPECTACULAR_SETTINGS
from storage.models.files import files_storage
from users.serializers import users as users_s


User = get_user_model()


@extend_schema(tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['ADMIN']])
@extend_schema_view(
    list=extend_schema(summary='Получение списка пользователей, зарегистрированных в системе'),
    retrieve=extend_schema(summary='Данные пользователя', ),
    update=extend_schema(summary='Полное изменение данных пользователя', ),
    partial_update=extend_schema(summary='Частичное изменение данных пользователя', ),
    destroy=extend_schema(summary='Удаление пользователя', ),
)
class UsersViewSet(RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser, )
    serializer_class = users_s.UsersUpdateSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return users_s.UsersUpdateSerializer
        return users_s.UsersListSerializer
