import csv

from django.core.management import BaseCommand

from recipes.models import Ingredients, Tags

MODELS_FILES = {
    Ingredients: 'ingredients.csv',
    Tags: 'tags.csv',
}

class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file in MODELS_FILES.items():
            with open(
                f'static/data/{file}',
                'r', encoding='utf-8',
            ) as table:
                reader = csv.DictReader(table)
                model.objects.bulk_create(model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS(
            '=== Ингредиенты и теги успешно загружены ===')
        )
