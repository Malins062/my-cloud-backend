import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )

    @staticmethod
    def validate_username(value):
        if not re.match('^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
            raise ParseError(
                dict(
                    username=[f'Формат логина: только латинские буквы и цифры, первый символ - буква, длина от 4 до 20 '
                              f'символов'])
            )
        elif User.objects.filter(username=value).exists():
            raise ParseError(
                dict(username=[f'Пользователь с логином: {value} - уже зарегистрирован.'])
            )
        return value

    @staticmethod
    def validate_email(value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                dict(email=[f'Пользователь с адресом электронной почты: {email} - уже зарегистрирован.'])
            )
        return email

    @staticmethod
    def validate_password(value):
        if not re.match('(?=^.{6,}$)(?=.*\d+)(?=.*[\W_]+)(?![.\n])(?=.*[A-ZА-Я]+)(?=.*[a-z]*).*$', value):
            raise ParseError(
                dict(
                    password=[f'Формат пароля: не менее 6 символов, как минимум одна заглавная буква, одна цифра и один'
                              f'спецсимвол'])
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined',
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )

    def validate(self, attrs):
        user = self.instance
        password = attrs.pop('old_password') if 'old_password' in attrs else None
        if not user.check_password(password):
            raise ParseError(
                {'password': ['Проверьте правильность текущего пароля.']}
            )
        return attrs

    @staticmethod
    def validate_new_password(value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('new_password') if 'new_password' in validated_data else None
        instance.set_password(password)
        instance.save()
        return instance
