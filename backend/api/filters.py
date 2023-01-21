from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Кастомный фильтр для рецептов."""
    author = filters.CharFilter(
        field_name='author',
        method='get_filter_field'
    )
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='get_filter_field'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='get_filter_field'
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_filter_field(self, queryset, name, value):
        filter_dict = {
            'is_favorited':
                queryset.filter(favorite__user=self.request.user),
            'is_in_shopping_cart':
                queryset.filter(shoppingcart__user=self.request.user),
            'author':
                queryset.filter(author=self.request.user)
                if value == 'me' else queryset.filter(author__id=value)
        }

        return filter_dict[name] if value else queryset
