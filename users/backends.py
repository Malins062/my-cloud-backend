from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = True
    supports_inactive_user = True

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def authenticate(request, username, password):
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email=username)
            )
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None
