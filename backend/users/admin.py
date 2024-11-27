from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users.models import Follow, FoodgramUser

User = get_user_model()


admin.site.unregister(Group)


@admin.register(FoodgramUser)
class FoodgramUserAdmin(admin.ModelAdmin):
    """Создание объекта пользователя в админ панели."""

    list_display = [
        'username', 'email', 'first_name', 'last_name'
    ]
    list_display_links = ['username', 'email']
    list_filter = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    empty_value_display = 'Поле не заполнено'


@admin.register(Follow)
class SubscriptionAdmin(admin.ModelAdmin):
    """Создание объекта подписки в админ панели."""

    list_display = ['id', 'user', 'author']
    list_display_links = ['id', 'user']
    search_fields = ('author',)
    empty_value_display = 'Поле не заполнено'
