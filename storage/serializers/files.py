from django.contrib.auth import get_user_model
from rest_framework import serializers

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


class FilesDeleteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=True)

    class Meta(FilesSerializer.Meta):
        pass
