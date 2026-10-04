"""Команда добавления пользователя в группу «Менеджер»."""

from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    """Добавляет пользователя в группу «Менеджер»."""

    help = "Добавляет пользователя в группу «Менеджер» по email"

    def add_arguments(self, parser: Any) -> None:
        """Добавляет аргументы командной строки."""
        parser.add_argument("--email", type=str, required=True)
        parser.add_argument("--password", type=str, required=True)

    def handle(self, *args: Any, **options: Any) -> None:
        """Создаёт или обновляет пользователя и добавляет его в группу."""
        email = options["email"]
        password = options["password"]

        user, created = CustomUser.objects.get_or_create(email=email)
        user.set_password(password)
        user.is_staff = True
        user.save()

        group, _ = Group.objects.get_or_create(name="Менеджер")
        user.groups.add(group)

        action = "создан" if created else "обновлён"
        self.stdout.write(self.style.SUCCESS(f"Пользователь {email} {action} и добавлен в группу «Менеджер»."))