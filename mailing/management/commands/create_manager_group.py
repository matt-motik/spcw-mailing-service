"""Команда создания группы «Менеджер»."""

from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создаёт группу «Менеджер» и назначает ей права."""

    help = "Создаёт группу «Менеджер» с правами просмотра и отключения рассылок"

    def handle(self, *args: Any, **options: Any) -> None:
        """Создаёт группу и назначает права."""
        group, _ = Group.objects.get_or_create(name="Менеджер")

        codenames = [
            "view_recipient",
            "view_message",
            "view_mailing",
            "view_mailingattempt",
            "view_customuser",
            "change_customuser",
            "can_disable_mailing",
        ]
        permissions = Permission.objects.filter(codename__in=codenames)
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(f"Группе «Менеджер» назначено прав: {permissions.count()}."))
