from django.contrib.auth import get_user_model
from rest_framework import serializers

from storage.models.files import File

User = get_user_model()


class FileSerializer(serializers.ModelSerializer):
    file_name = serializers.CharField()
    comment = serializers.CharField(allow_null=True)

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
