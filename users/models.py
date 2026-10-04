"""Модели данных приложения users."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from config.validators import validate_image_file
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.

    Авторизация по email вместо username. Дополнительно хранит аватар
    и страну проживания.

    Attributes:
        email (EmailField): Уникальный email, используется для входа.
        avatar (ImageField): Изображение профиля (опционально).
        country (CharField): Страна проживания (опционально).
    """

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Используется для входа в систему.",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Аватар",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    objects = CustomUserManager()

    class Meta:
        """Мета-параметры модели CustomUser."""

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        """
        Возвращает строковое представление пользователя.

        Returns:
            str: Email пользователя.
        """
        return str(self.email)