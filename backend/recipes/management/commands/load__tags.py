from django.core.management import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = 'Загружаем тэги'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#E26C2D', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#0ecf0a', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#1404c7', 'slug': 'dinner'},
            {'name': 'Закуски', 'color': '#8775D2', 'slug': 'snacks'},
        ]
        Tag.objects.bulk_create(Tag(**tag) for tag in data)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены!'))
