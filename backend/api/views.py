from django.shortcuts import render

from .mixins import CreateListDestroyViewSet
from recipes.models import Recipe, Tag, Ingredient

