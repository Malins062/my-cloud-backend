import os
import re

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.http import FileResponse

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet

from config.settings import SPECTACULAR_SETTINGS
from storage.serializers import files as files_s
from storage.models.files import File


User = get_user_model()


@extend_schema(
    tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['STORAGE']],
    parameters=[
        OpenApiParameter(
            name='user_id',
            type=int,
            location=OpenApiParameter.QUERY,
            description='Идентификатор пользователя (только для администраторов)',
            required=False
        )
    ]
)
@extend_schema_view(
    list=extend_schema(summary='Получение списка файлов текущего пользователя'),
    post=extend_schema(summary='Загрузка файла для текущего пользователя'),
    retrieve=extend_schema(summary='Информация о файле',
                           parameters=[
                               OpenApiParameter(
                                   name='download',
                                   type=bool,
                                   location=OpenApiParameter.QUERY,
                                   description='Запрос на скачивание файла',
                                   required=False
                               )
                           ]),
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
    permission_classes = (IsAuthenticated, )
    serializer_class = files_s.FilesSerializer

    def get_serializer_class(self):
        match self.request.method:
            case 'PATCH': return files_s.FilesUpdateSerializer
            case 'DELETE': return files_s.FilesDeleteSerializer
            case _: return files_s.FilesSerializer

    def get_query_user(self):
        user = self.request.user
        user_id = self.request.query_params.get('user_id')  # Получаем user_id из query параметров
        if user_id:
            if not user.is_staff:
                raise PermissionDenied('Отказано в доступе. Необходимо иметь статус администратора.')
            else:
                try:
                    user = User.objects.get(id=user_id)
                except Exception:
                    raise NotFound(f'Пользователь с идентификатором #{user_id} не существует.')
        return user

    def get_queryset(self):
        serializer = files_s.FilesSerializer(data=self.request.data)
        queryset = super(FilesViewSet, self).get_queryset()
        user = self.get_query_user()
        return queryset.filter(owner=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        is_download = self.request.query_params.get('download')  # Получаем download из query параметров
        if is_download:
            return self.download_file(pk=instance.id)
        else:
            return Response(serializer.data)

    def perform_create(self, serializer):
        file = serializer.validated_data.get('file')
        new_file_name = os.path.basename(file.name)
        if File.objects.filter(file_name=new_file_name,
                               owner=self.get_query_user()).exists():
            raise ValidationError(f'Файл с именем: {new_file_name} - уже существует в системе.')
        serializer.save(owner=self.get_query_user())

    def update(self, request, *args, **kwargs):
        serializer = files_s.FilesUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        instance = self.get_object()
        response_status = HTTP_200_OK
        response_messages = None

        new_file_name = request.data.get('file_name')
        if new_file_name:
            if File.objects.filter(file_name=new_file_name, owner=self.get_query_user()).exists():
                raise ValidationError(f'Файл с именем: {new_file_name} - уже существует в системе.')

            old_file_path = instance.file.path
            new_file_path = os.path.join(os.path.dirname(old_file_path), new_file_name)

            try:
                os.rename(old_file_path, new_file_path)
                instance.file.name = new_file_path
                instance.file_name = new_file_name
                instance.save()
                response_messages = {'message': 'Файл переименован.'}
            except Exception as e:
                response_messages = {'error': str(e)}
                response_status = HTTP_400_BAD_REQUEST

        new_comment = request.data.get('comment')
        if new_comment:

            try:
                instance.comment = new_comment
                instance.save()
                response_messages += {'message': 'Комментарий к файлу изменен.'}
            except Exception as e:
                response_messages += {'error': str(e)}
                response_status = HTTP_400_BAD_REQUEST

        return Response(response_messages, status=response_status)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            file = File.objects.get(id=instance.id)
            file_path = file.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
                file.delete()
                self.perform_destroy(instance)
                return Response({'message': 'Файл удален'}, status=HTTP_204_NO_CONTENT)
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        except File.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

    @staticmethod
    def download_file(pk):
        file_instance = File.objects.get(pk=pk)
        file_path = file_instance.file.path

        try:
            # Открываем файл и отправляем его как FileResponse
            file_to_download = open(file_path, 'rb')
            response = FileResponse(file_to_download)
            response['Content-Disposition'] = 'attachment; filename=' + file_instance.file.name
            return response
        except FileNotFoundError:
            return Response({"error": "File not found"}, status=HTTP_404_NOT_FOUND)
