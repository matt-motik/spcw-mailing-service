"""Сервисные функции приложения mailing."""

import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from mailing.models import Mailing, MailingAttempt


def update_status(mailing: Mailing) -> None:
    """
    Пересчитывает и сохраняет статус рассылки.

    Сравнивает текущее время с start_time и end_time и обновляет
    статус в БД, если он отличается от вычисленного.

    Args:
        mailing: Рассылка, для которой нужно обновить статус.
    """
    now = timezone.now()

    if now < mailing.start_time:
        new_status = Mailing.STATUS_CREATED
    elif now > mailing.end_time:
        new_status = Mailing.STATUS_FINISHED
    else:
        new_status = Mailing.STATUS_STARTED

    if mailing.status != new_status:
        mailing.status = new_status
        mailing.save(update_fields=["status", "updated_at"])


def send_mailing(mailing: Mailing) -> tuple[int, int]:
    """
    Отправляет рассылку всем получателям.

    Проверяет окно отправки, для каждого получателя вызывает send_mail,
    собирает объекты попыток и создаёт их одним batch через bulk_create.

    Args:
        mailing: Рассылка для отправки.

    Returns:
        tuple[int, int]: Количество успешных и неуспешных попыток.

    Raises:
        ValueError: Если текущее время вне окна start_time–end_time
            или рассылка отключена менеджером.
    """
    now = timezone.now()
    if not (mailing.start_time <= now <= mailing.end_time):
        raise ValueError("Текущее время вне окрестности рассылки.")

    if mailing.is_disabled:
        raise ValueError("Рассылка отключена менеджером.")

    attempts: list[MailingAttempt] = []
    success = 0
    failure = 0

    for recipient in mailing.recipients.all():
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            attempts.append(
                MailingAttempt(
                    mailing=mailing,
                    status=MailingAttempt.STATUS_SUCCESS,
                    server_response="OK",
                )
            )
            success += 1
        except (smtplib.SMTPException, OSError) as exc:
            attempts.append(
                MailingAttempt(
                    mailing=mailing,
                    status=MailingAttempt.STATUS_FAILURE,
                    server_response=str(exc),
                )
            )
            failure += 1

    MailingAttempt.objects.bulk_create(attempts)
    return success, failure
