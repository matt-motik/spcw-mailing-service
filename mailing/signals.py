"""Сигналы приложения mailing."""

from typing import Any

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from mailing.models import Mailing, MailingAttempt, Recipient


@receiver([post_save, post_delete], sender=Mailing)
def invalidate_index_stats_on_mailing(sender: type[Mailing], instance: Mailing, **kwargs: Any) -> None:
    """
    Сбрасывает кеш статистики главной при изменении рассылки.

    Args:
        sender: Класс модели, отправившей сигнал.
        instance: Сохранённая или удалённая рассылка.
        **kwargs: Дополнительные аргументы сигнала.
    """
    cache.delete("index_stats")
    cache.delete(f"stats:user:{instance.owner_id}")


@receiver([post_save, post_delete], sender=Recipient)
def invalidate_index_stats_on_recipient(sender: type[Recipient], instance: Recipient, **kwargs: Any) -> None:
    """
    Сбрасывает кеш статистики главной при изменении получателя.

    Args:
        sender: Класс модели, отправившей сигнал.
        instance: Сохранённый или удалённый получатель.
        **kwargs: Дополнительные аргументы сигнала.
    """
    cache.delete("index_stats")
    cache.delete(f"stats:user:{instance.owner_id}")


@receiver([post_save, post_delete], sender=MailingAttempt)
def invalidate_stats_on_attempt(sender: type[MailingAttempt], instance: MailingAttempt, **kwargs: Any) -> None:
    """
    Сбрасывает кеш статистики владельца рассылки при изменении попытки.

    Args:
        sender: Класс модели, отправившей сигнал.
        instance: Сохранённая или удалённая попытка.
        **kwargs: Дополнительные аргументы сигнала.
    """
    cache.delete(f"stats:user:{instance.mailing.owner_id}")