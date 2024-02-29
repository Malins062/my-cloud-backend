from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from storage.models.files import File

User = get_user_model()


class FilesSerializer(serializers.ModelSerializer):
    # user_id = serializers.CharField(allow_null=True)
    # file_id = serializers.CharField(allow_null=True)
    # file = serializers.FileField(allow_null=True)

    class Meta:
        model = File
        fields = '__all__'
        # fields = (
        #     '__all__',
        # )


class FilesUpdateSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField(allow_null=True)
    comment = serializers.CharField(allow_null=True)

    class Meta(FilesSerializer.Meta):
        fields = (
            'file_name',
            'comment',
        )

    @staticmethod
    def validate_either_or(value):
        if not value.get('file_name') and not value.get('comment'):
            raise ValidationError('Хотя бы одно из полей (file_name, comment) должно быть заполнено.')

    def validate(self, data):
        self.validate_either_or(data)
        return data


class FilesDeleteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)

    class Meta(FilesSerializer.Meta):
        pass
