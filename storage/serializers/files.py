import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from storage.models.files import File

User = get_user_model()


class FilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = (
            'id',
            'file',
            'file_name',
            'file_size',
            'comment',

            'uploaded_at',
            'modified_at',
        )


class FilesUpdateSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(allow_null=True)
    comment = serializers.CharField(allow_null=True)

    class Meta(FilesSerializer.Meta):
        pass

    @staticmethod
    def validate_file_name(value):
        # if not re.match(r'^(?!.[<>:"/\|?]).{1,255}$', value):
        #     raise ValidationError(f'Неверный формат имени файла.')
        if File.objects.filter(file_name=value).exists():
            raise ValidationError(f'Файл с именем: {value} - уже существует.')
        return value


class FilesDeleteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)

    class Meta(FilesSerializer.Meta):
        pass
