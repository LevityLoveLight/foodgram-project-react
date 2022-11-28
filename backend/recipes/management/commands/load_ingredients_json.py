import json
import os

from django.core.management import BaseCommand
from django.conf import settings

from recipes.models import Ingredient

JSON_DATA_FILE = os.path.join(settings.BASE_DIR, 'data/ingredients.json')


class Command(BaseCommand):
    help = 'Загружаем ингридиенты'

    def handle(self, *args, **options):
        ingredients = open(JSON_DATA_FILE, 'r', encoding='utf-8')
        json_data = json.load(ingredients)
        Ingredient.objects.bulk_create(
            [Ingredient(**item) for item in json_data]
        )
        self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))