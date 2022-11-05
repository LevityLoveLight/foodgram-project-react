from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()

COOCKING_MIN_TIME = 1
INGREDIENTS_MIN_QUANTITY = 0.25


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=64,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True
        )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тэг'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=256,
        unique=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерени',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ингридиент'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование рецепта'
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/pictures',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(COOCKING_MIN_TIME,
                              'Минимальное время одна минута!')
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Ингридиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингрдиентов',
        validators=[
            MinValueValidator(INGREDIENTS_MIN_QUANTITY, 'Минимальное количество 0.25!')
        ]
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингредиентов'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorites_user',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='fovorites_recipe',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Любимый рецепт'

    def __str__(self):
        return self.user


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Покупка'

    def __str__(self):
        return f'{self.user} {self.recipe}'