"""Команда создания группы «Пользователь»."""

from typing import Any

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создаёт группу «Пользователь»."""

    help = "Создаёт группу «Пользователь»"

    def handle(self, *args: Any, **options: Any) -> None:
        """Создаёт группу, если её нет."""
        group, created = Group.objects.get_or_create(name="Пользователь")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа «Пользователь» создана."))
        else:
            self.stdout.write(self.style.WARNING("Группа «Пользователь» уже существует."))
