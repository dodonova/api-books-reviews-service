from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.validators import validate_username_not_me
from api_yamdb.settings import (
    USERNAME_MAX_LENTH,
    EMAIL_MAX_LENGTH
)


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    ]
    username = models.CharField(
        max_length=USERNAME_MAX_LENTH,
        unique=True,
        validators=([
            RegexValidator(
                regex=r'^[\w.@+-]+$'
            ),
            validate_username_not_me
        ])
    )
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH,
                              unique=True)
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        help_text='Код подтверждения пользователя',
        max_length=200,
    )
    role = models.CharField(
        'Роль',
        help_text='Роль пользователя',
        max_length=max([len(i[1]) for i in USER_ROLES]),
        choices=USER_ROLES,
        default=USER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username
