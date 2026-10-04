"""Настройки административной панели приложения mailing."""

from django.contrib import admin

from mailing.models import Mailing, MailingAttempt, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    """Настройки административной панели получателей."""

    list_display = ("full_name", "email", "created_at")
    search_fields = ("full_name", "email")
    ordering = ("full_name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Настройки административной панели сообщений."""

    list_display = ("subject", "created_at")
    search_fields = ("subject",)
    ordering = ("-created_at",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    """Настройки административной панели рассылок."""

    list_display = ("__str__", "status", "start_time", "end_time", "owner")
    list_filter = ("status",)
    search_fields = ("message__subject",)
    filter_horizontal = ("recipients",)
    ordering = ("-created_at",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    """Настройки административной панели попыток рассылок."""

    list_display = ("mailing", "status", "attempt_time")
    list_filter = ("status",)
    ordering = ("-attempt_time",)