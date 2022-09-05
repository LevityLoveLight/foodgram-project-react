from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True
        )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(max_length=256)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    description = models.TextField(
        'Описание'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(1, 'Минимальное время одна минута!')
        ]
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True
    )
    units_of_measure = models.CharField(
        max_length=10
    )

    def __str__(self):
        return self.name