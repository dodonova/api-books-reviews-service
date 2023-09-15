from django.db import models
from .validators import validate_pattern_symbols, max_length
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                validators=[validate_pattern_symbols])
    email = models.EmailField(max_length=254,
                              blank=False,
                              unique=True,
                              validators=[max_length])
    bio = models.TextField(max_length=150, blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения',
        help_text='Код подтверждения пользователя',
        max_length=200,
    )
    role = models.CharField(
        'Роль',
        help_text='Роль пользователя',
        max_length=150,
        blank=False,
        choices=USER_ROLES,
        default='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return self.username
