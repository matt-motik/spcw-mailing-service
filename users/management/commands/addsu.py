"""Management-команда для создания суперпользователя по email."""

from typing import Any

from django.core.management.base import BaseCommand, CommandParser
from django.db.utils import IntegrityError

from users.models import CustomUser


class Command(BaseCommand):
    """Создаёт суперпользователя с указанными email и паролем.

    Если пользователь с таким email уже существует — обновляет ему
    пароль и флаги is_staff/is_superuser.

    Example:
        python manage.py addsu --email=admin@example.com --password=secret123
    """

    help = "Создаёт суперпользователя по email и паролю"

    def add_arguments(self, parser: CommandParser) -> None:
        """Добавляет аргументы командной строки.

        Args:
            parser: Парсер аргументов Django.
        """
        parser.add_argument(
            "--email",
            type=str,
            required=True,
            help="Email суперпользователя",
        )
        parser.add_argument(
            "--password",
            type=str,
            required=True,
            help="Пароль суперпользователя",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Создаёт или обновляет суперпользователя.

        Args:
            *args: Позиционные аргументы (не используются).
            **options: Опции команды, включая email и password.
        """
        email: str = options["email"]
        password: str = options["password"]

        try:
            user, created = CustomUser.objects.get_or_create(email=email)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
        except IntegrityError as exc:
            self.stderr.write(self.style.ERROR(f"Ошибка создания: {exc}"))
            return

        if created:
            self.stdout.write(self.style.SUCCESS(f"Суперпользователь {email} создан"))
        else:
            self.stdout.write(self.style.WARNING(f"Пользователь {email} уже существовал — обновлён"))
