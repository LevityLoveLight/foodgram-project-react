from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 150


class User(AbstractUser):

    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_LENGTH,
        blank=True,
        unique=True
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=MAX_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_LENGTH,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_LENGTH,
        blank=False,
    )

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username


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
        ordering = ('id',)

    def __str__(self):
        return f' Пользователь{self.user} подписан на {self.author}'
