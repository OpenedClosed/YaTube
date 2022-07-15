from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import role_validate, username_validate


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'), ]
    username = models.CharField(max_length=150,
                                unique=True,
                                validators=[username_validate],
                                verbose_name='Имя пользователя')
    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='Адрес электронной почты')
    first_name = models.CharField(max_length=150,
                                  blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                 blank=True,
                                 verbose_name='Фамилия')
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.TextField(choices=ROLE_CHOICES,
                            default=USER,
                            validators=[role_validate],
                            verbose_name='Роль пользователя')

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
