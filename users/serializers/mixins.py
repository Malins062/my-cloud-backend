import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserMixinSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )

    @staticmethod
    def validate_username(value):
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
            raise ValidationError(f'Формат логина: только латинские буквы и цифры, первый символ - буква, длина от 4 '
                                  f'до 20 символов')
        elif User.objects.filter(username=value).exists():
            raise ValidationError(f'Пользователь с логином: {value} - уже зарегистрирован.')
        return value

    @staticmethod
    def validate_email(value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(f'Пользователь с адресом электронной почты: {email} - уже зарегистрирован.')
        return email
