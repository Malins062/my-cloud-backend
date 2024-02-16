from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers.mixins import UserMixinSerializer


User = get_user_model()


class UsersListSerializer(serializers.ModelSerializer):
    class Meta(UserMixinSerializer.Meta):
        fields = UserMixinSerializer.Meta.fields + ('id',
                                                    'date_joined',
                                                    'last_login',
                                                    'is_staff', )


class UsersUpdateSerializer(UserMixinSerializer):

    class Meta(UserMixinSerializer.Meta):
        fields = UserMixinSerializer.Meta.fields + ('is_staff',)
