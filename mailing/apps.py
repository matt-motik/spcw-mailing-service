"""Конфигурация приложения mailing."""

from django.apps import AppConfig


class MailingConfig(AppConfig):
    """Конфигурация приложения рассылок."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"
    verbose_name = "Рассылки"