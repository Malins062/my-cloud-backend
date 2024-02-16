import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from users.serializers.mixins import UserMixinSerializer


User = get_user_model()


class RegistrationSerializer(UserMixinSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta(UserMixinSerializer.Meta):
        fields = UserMixinSerializer.Meta.fields + ('password',)

    @staticmethod
    def validate_password(value):
        if not re.match(r'(?=^.{6,}$)(?=.*\d+)(?=.*[\W_]+)(?![.\n])(?=.*[A-ZА-Я]+)(?=.*[a-z]*).*$', value):
            raise ParseError(
                dict(
                    password=[f'Формат пароля: не менее 6 символов, как минимум одна заглавная буква, одна цифра и один'
                              f'спецсимвол'])
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileListSerializer(UserMixinSerializer):
    class Meta(UserMixinSerializer.Meta):
        fields = UserMixinSerializer.Meta.fields + ('id', 'data_joined', )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta(UserMixinSerializer.Meta):
        fields = UserMixinSerializer.Meta.fields


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
