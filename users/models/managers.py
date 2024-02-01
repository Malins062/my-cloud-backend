from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, password=None, username=None,
                     first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ParseError('Укажите адрес электронной почты!')
        email = self.normalize_email(email)

        if not first_name:
            raise ParseError('Укажите имя пользователя!')
        first_name = first_name.strip()

        if not last_name:
            raise ParseError('Укажите фамилию пользователя!')
        last_name = last_name.strip()

        if not username:
            username = email

        user = self.model(username=username, **extra_fields)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, username=None,
                    first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, username, first_name, last_name, **extra_fields)

    def create_superuser(self, email=None, password=None, username=None,
                         first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, username, first_name, last_name, **extra_fields)