from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from config.settings import SPECTACULAR_SETTINGS
from storage.serializers import files as files_s
from storage.models.files import File


User = get_user_model()


@extend_schema(tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['STORAGE']])
@extend_schema_view(
    list=extend_schema(summary='Получение списка файлов текущего пользователя'),
    retrieve=extend_schema(summary='Информация о файле', ),
    partial_update=extend_schema(summary='Изменение информации о файле', ),
    destroy=extend_schema(summary='Удаление файла', ),
)
class FilesViewSet(RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = File.objects.all()
    # queryset = File.objects.filter(owner=User)
    permission_classes = (IsAuthenticated, )
    serializer_class = files_s.FileSerializer

    # def get_serializer_class(self):
    #     if self.request.method in ['PUT', 'PATCH', 'DELETE']:
    #         return users_s.UsersUpdateSerializer
    #     return users_s.UsersListSerializer
