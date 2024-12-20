from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag

User = get_user_model()


class RecipeFilter(FilterSet):
    """Фильтр для отображения избранного и списка покупок."""

    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = filters.BooleanFilter(method='favorite_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='shopping_cart_filter'
    )

    def favorite_filter(self, queryset, name, value):
        """Фильтр для избранного."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user_id=user.id)
        return queryset

    def shopping_cart_filter(self, queryset, name, value):
        """Фильтр для списка покупок."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_recipe__user_id=user.id)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')
