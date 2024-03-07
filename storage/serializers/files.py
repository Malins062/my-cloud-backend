import re

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.fields import empty

from storage.models.files import File

User = get_user_model()


class FilesListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False,
                                       validators=[MinValueValidator(1)])

    def run_validation(self, data=empty):
        unknown_fields = set(data.keys()) - set(self.fields.keys())
        if unknown_fields:
            raise serializers.ValidationError(f'Лишние поля в запросе: {", ".join(unknown_fields)}')

        return super().run_validation(data)


class FilesRetrieveSerializer(FilesListSerializer):
    ACTION_CHOICES = {
        'download': 'Download file',
        'get_link': 'Get a link to download the file',
        'remove_link': 'Remove link'
    }
    action = serializers.ChoiceField(required=False,
                                     choices=ACTION_CHOICES)


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class FilesUpdateSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(required=False)
    comment = serializers.CharField(required=False)

    class Meta(FilesSerializer.Meta):
        fields = (
            'file_name',
            'comment',
        )

    @staticmethod
    def validate_at_least_one_field(value):
        if not any(value.values()):
            raise ValidationError('Хотя бы одно из полей (file_name, comment) должно быть заполнено.')

    @staticmethod
    def validate_file_name(value):
        if not re.match(r'^[\w\s-]+(\.[\w\s-]+)*$', value):
            raise ValidationError(f'Неверный формат имени файла: {value}')
        return value

    def validate(self, data):
        self.validate_at_least_one_field(data)
        return data


class FilesDeleteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)

    class Meta(FilesSerializer.Meta):
        pass
