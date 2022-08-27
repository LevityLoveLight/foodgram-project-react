from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
        verbose_name='Описание'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    cooking_time = TimeField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    quantity = models.FloatFild()
    units_of_measure =

    def __str__(self):
        return self.name