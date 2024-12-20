from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint

NAME_MAX_LENGTH = 150
EMAIL_MAX_LENGTH = 254


DEFAULT_AVATAR = 'users/avatar_default.jpg'


class FoodgramUser(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        'Никнейм',
        max_length=NAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(),)
    )
    first_name = models.CharField(
        'Имя', max_length=NAME_MAX_LENGTH,
    )
    last_name = models.CharField(
        'Фамилия', max_length=NAME_MAX_LENGTH
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
    )
    avatar = models.ImageField(
        'Аватар профиля',
        upload_to='users',
        blank=True,
        null=True,
        default=DEFAULT_AVATAR
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('username', 'email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:50]

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name


class Follow(models.Model):
    """Модель подписчиков."""

    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='publisher',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user__username',)
        constraints = (
            UniqueConstraint(
                fields=('author', 'user'), name='unique_following',
            ),
            CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='user_is_not_author',
            ),
        )

    def __str__(self):
        return f'{self.user.username} подписался на {self.author.username}'
