from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models.managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=320, unique=True, null=False, blank=False,
        help_text='Адрес электронной почты. Обязательное поле. Не более 320 символов.',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=60, blank=False, null=False,
        help_text='Имя пользователя. Обязательное поле. Не более 60 символов.',
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=120, blank=False, null=False,
        help_text='Фамилия пользователя. Обязательное поле. Не более 120 символов.',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', ]

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    full_name.fget.short_description = 'Полное имя'

    def __str__(self):
        return f'{self.full_name} #{self.pk}'
