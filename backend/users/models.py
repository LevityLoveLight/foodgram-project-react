from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 64


class User(AbstractUser):

    login = models.CharField(
        'Логин',
        max_length=MAX_LENGTH,
        blank=True,
        unique=True
    )
    password = models.CharField(
        'Пароль',
        max_length=MAX_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        'E-mail',
        max_length=MAX_LENGTH,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH,
        blank=False,
    )
    middle_name = models.CharField(
        'Отчество',
        max_length=MAX_LENGTH,
        blank=False,
    )

    Last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH,
        blank=False,
    )

    REQUIRED_FIELDS = ['login', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.login


class Follow(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    class Meta:
        verbose_name = 'Подписка'
