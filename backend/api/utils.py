import datetime

from django.conf import settings
from django.db.models.aggregates import Sum

from recipes.models import IngredientAmount


def make_shopping_list(user):
    current_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
    text_lines = (
        'Список покупок продуктов\n'
        f'список сформирован на - {current_date}\n\n'
    )
    ingredients = IngredientAmount.objects.filter(
        recipe__cart__user=user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).order_by(
        'ingredient__name'
    ).annotate(
        total_amount=Sum('amount')
    )

    for item in ingredients:
        format_string = (
            settings.CART_INGREDIENTS_FORMAT.format(
                name=item['ingredient__name'],
                measurement_unit=item['ingredient__measurement_unit'],
                total=item['total_amount']
            )
        )
        text_lines += f'{format_string}\n'

    return text_lines
