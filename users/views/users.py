from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from config.settings import SPECTACULAR_SETTINGS
from users.serializers import users as users_s

User = get_user_model()


@extend_schema_view(
    get=extend_schema(
        summary='Получение списка пользователей системы',
        tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['ADMIN']],
        description='Получение списка пользователей системы (только для администраторов)',
    ),
)
class UsersListView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser, )
    serializer_class = users_s.UsersListSerializer
