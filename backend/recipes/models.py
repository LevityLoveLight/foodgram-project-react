from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .foodgram import settings

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
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
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
    tag = models.ManyToManyField(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(COOCKING_MIN_TIME, 'Минимальное время одна минута!')
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

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингрдиентов',
        validators=[
            MinValueValidator(INGREDIENTS_MIN_QUANTITY, 'Минимальное количество 0.25!')
        ]
    )


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    class Meta:
        verbose_name = 'Покупка'


    def __str__(self):
        return self.user.username