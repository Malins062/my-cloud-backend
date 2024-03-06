from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response

from config.settings import SPECTACULAR_SETTINGS
from common.mixins import get_unique_str, get_query_user
from storage.models.files import File
from storage.serializers import files as files_s


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
class UniqueLinkView(APIView):
    queryset = File.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = files_s.FilesSerializer

    @extend_schema(
        summary='Получить ссылку/доступ на скачивания файла',
        parameters=[
            OpenApiParameter(
                name='file_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Запрос на скачивание файла',
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        user = get_query_user(self)
        file_id = request.data.get('file_id')
        queryset = File.objects.get(pk=file_id, owner=user)
        if file_id:
            if queryset:
                raise ValidationError(f'Файл с идентификатором: #{file_id} - не существует в системе.')
            else:
                try:
                    public_link = get_unique_str(50)
                    queryset.public_link = public_link
                    queryset.save()
                    return Response({'public_link': f'{public_link}'}, status=HTTP_200_OK)
                except Exception as e:
                    Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        else:
            raise ValidationError('Get-параметр file_id обязателен для заполнения.')
