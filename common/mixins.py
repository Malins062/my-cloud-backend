import uuid

from django.contrib.auth import get_user_model

from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError

User = get_user_model()


def get_query_user(instance):
    user = instance.request.user
    user_id = instance.request.query_params.get('user_id')  # Получаем user_id из query параметров
    if user_id:
        if not user.is_staff:
            raise PermissionDenied('Отказано в доступе. Необходимо иметь статус администратора.')
        else:
            try:
                user = User.objects.get(id=user_id)
            except Exception:
                raise NotFound(f'Пользователь с идентификатором #{user_id} не существует.')
    return user


def replace_query_params(params):
    query_params = {key: value[0] if isinstance(value, list) else value for key, value in params.items()}
    return query_params


def get_unique_str(length) -> str:
    unique_string = str(uuid.uuid4()).replace('-', '')[:length]
    return unique_string

