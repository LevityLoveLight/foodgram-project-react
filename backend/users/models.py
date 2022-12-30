from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    ADMIN = 'admin'
    USER = 'user'
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (USER, 'user'),
    )
    email = models.EmailField(
        verbose_name='Электр. почта',
        unique=True,
        max_length=254,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        default=USER,
        max_length=9,
    )

    class Meta:
        ordering = ('role', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.role == self.ADMIN

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

    def __str__(self):
        return f'{self.following.username} подписан на {self.user.username}'
