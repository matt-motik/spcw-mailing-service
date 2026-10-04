"""Менеджеры моделей приложения users."""

from typing import TYPE_CHECKING, Any

from django.contrib.auth.models import UserManager

if TYPE_CHECKING:
    from users.models import CustomUser


class CustomUserManager(UserManager):
    """Менеджер пользователей, использующий email вместо username."""

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        """
        Создаёт и сохраняет обычного пользователя.

        Args:
            email: Email пользователя (используется как идентификатор).
            password: Пароль в открытом виде (будет захеширован).
            **extra_fields: Дополнительные поля модели пользователя.

        Returns:
            CustomUser: Созданный пользователь.

        Raises:
            ValueError: Если email не передан.
        """
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> "CustomUser":
        """
        Создаёт и сохраняет суперпользователя.

        Args:
            email: Email пользователя.
            password: Пароль в открытом виде.
            **extra_fields: Дополнительные поля модели пользователя.

        Returns:
            CustomUser: Созданный суперпользователь.

        Raises:
            ValueError: Если email не передан или не заданы is_staff/is_superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True")

        return self.create_user(email, password, **extra_fields)