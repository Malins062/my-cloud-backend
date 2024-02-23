import os

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from config.settings import SPECTACULAR_SETTINGS
from storage.serializers import files as files_s
from storage.models.files import File


User = get_user_model()


@extend_schema(tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['STORAGE']])
@extend_schema_view(
    list=extend_schema(summary='Получение списка файлов текущего пользователя'),
    post=extend_schema(summary='Загрузка файла для текущего пользователя'),
    retrieve=extend_schema(summary='Информация о файле', ),
    partial_update=extend_schema(summary='Изменение информации о файле', ),
    destroy=extend_schema(summary='Удаление файла', ),
)
class FilesViewSet(RetrieveModelMixin,
                   CreateModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = File.objects.all()
    # queryset = File.objects.filter(owner=User)
    permission_classes = (IsAuthenticated, )
    serializer_class = files_s.FilesSerializer

    def get_serializer_class(self):
        match self.request.method:
            case 'PATCH': return files_s.FilesUpdateSerializer
            case 'DELETE': return files_s.FilesDeleteSerializer
            case _: return files_s.FilesSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file = File.objects.get(id=instance.id)
            file_path = file.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
                file.delete()
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except File.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
