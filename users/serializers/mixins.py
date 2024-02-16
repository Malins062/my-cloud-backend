import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ParseError


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
            raise ParseError(
                dict(
                    username=[f'Username field format: only Latin letters and numbers, the first character is a '
                              f'letter, length from 4 to 20 characters.'])
            )
        elif User.objects.filter(username=value).exists():
            raise ParseError(
                dict(username=[f'The user with the username: {value} - is already registered.'])
            )
        return value

    @staticmethod
    def validate_email(value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                dict(email=[f'The user with the this email: {email} - is already registered.'])
            )
        return email
