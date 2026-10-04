"""Команда ручного запуска рассылок."""

from typing import Any

from django.core.management.base import BaseCommand
from django.utils import timezone

from mailing.models import Mailing
from mailing.services import send_mailing


class Command(BaseCommand):
    """Запускает все активные рассылки."""

    help = "Отправляет все рассылки, попадающие в окно start_time–end_time"

    def handle(self, *args: Any, **options: Any) -> None:
        """Находит активные рассылки и отправляет их."""
        now = timezone.now()
        mailings = Mailing.objects.filter(
            start_time__lte=now,
            end_time__gte=now,
            is_disabled=False,
        )

        if not mailings.exists():
            self.stdout.write(self.style.WARNING("Нет активных рассылок."))
            return

        for mailing in mailings:
            try:
                success, failure = send_mailing(mailing)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Рассылка #{mailing.pk}: успешно {success}, неудачно {failure}."
                    )
                )
            except ValueError as exc:
                self.stdout.write(self.style.ERROR(f"Рассылка #{mailing.pk}: {exc}"))