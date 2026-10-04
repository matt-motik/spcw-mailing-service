"""Конфигурация приложения mailing."""

from django.apps import AppConfig


class MailingConfig(AppConfig):
    """Конфигурация приложения рассылок."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"
    verbose_name = "Рассылки"

    def ready(self) -> None:
        """Регистрирует сигналы приложения."""
        from mailing import signals  # noqa: F401
