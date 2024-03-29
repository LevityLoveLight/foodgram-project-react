from csv import reader

from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(
                'api/data/tags.csv', 'r',
                encoding='UTF-8'
        ) as tags:
            for row in reader(tags):
                if len(row) == 3:
                    Tag.objects.get_or_create(
                        name=row[0], color=row[1], slug=row[2]
                    )
        self.stdout.write(
            self.style.SUCCESS('Тэги загружены'))
