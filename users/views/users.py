from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from config.settings import SPECTACULAR_SETTINGS
from users.serializers import users as users_s

User = get_user_model()


@extend_schema(tags=[SPECTACULAR_SETTINGS['TITLES_TAGS']['ADMIN']])
@extend_schema_view(
    list=extend_schema(summary='Получение списка пользователей, зарегистрированных в системе'),
    retrieve=extend_schema(summary='Данные пользователя', ),
    update=extend_schema(summary='Полное изменение данных пользователя', ),
    partial_update=extend_schema(summary='Частичное изменение данных пользователя', ),
    destroy=extend_schema(summary='Удаление пользователя', ),
)
class UsersViewSet(RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = users_s.UsersUpdateSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return users_s.UsersUpdateSerializer
        return users_s.UsersListSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Пользователь удален'}, status=HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_404_NOT_FOUND)
