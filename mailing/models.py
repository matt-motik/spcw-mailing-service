"""Модели данных приложения mailing."""
from django.conf import settings
from django.db import models


class Recipient(models.Model):
    """
    Модель получателя рассылки.

    Attributes:
        email (EmailField): Email получателя (уникальный).
        full_name (CharField): ФИО получателя.
        comment (TextField): Комментарий (необязательное поле).
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего изменения.
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipients",
        verbose_name="Владелец",
    )
    class Meta:
        """Мета-параметры модели Recipient."""

        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        ordering = ["full_name"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление получателя.

        Returns:
            str: ФИО и email получателя.
        """
        return f"{self.full_name} <{self.email}>"


class Message(models.Model):
    """
    Модель сообщения для рассылки.

    Attributes:
        subject (CharField): Тема письма.
        body (TextField): Тело письма.
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего изменения.
    """

    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="Владелец",
    )
    class Meta:
        """Мета-параметры модели Message."""

        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление сообщения.

        Returns:
            str: Тема письма.
        """
        return str(self.subject)


class Mailing(models.Model):
    """
    Модель рассылки.

    Attributes:
        start_time (DateTimeField): Дата и время начала отправки.
        end_time (DateTimeField): Дата и время окончания отправки.
        status (CharField): Статус рассылки (Создана / Запущена / Завершена).
        is_disabled (BooleanField): Признак отключения рассылки менеджером.
        message (ForeignKey): Сообщение для рассылки.
        recipients (ManyToManyField): Получатели рассылки.
        owner (ForeignKey): Пользователь, создавший рассылку.
        created_at (DateTimeField): Дата и время создания записи.
        updated_at (DateTimeField): Дата и время последнего изменения.
    """

    STATUS_CREATED = "Создана"
    STATUS_STARTED = "Запущена"
    STATUS_FINISHED = "Завершена"
    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_FINISHED, "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время начала")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус",
    )
    is_disabled = models.BooleanField(
        default=False,
        verbose_name="Отключена",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(
        Recipient,
        related_name="mailings",
        verbose_name="Получатели",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Владелец",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        """Мета-параметры модели Mailing."""

        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-created_at"]
        permissions = [("can_disable_mailing", "Может отключать рассылку")]

    def __str__(self) -> str:
        """
        Возвращает строковое представление рассылки.

        Returns:
            str: Тема сообщения и дата начала.
        """
        return f"{self.message.subject} ({self.start_time:%d.%m.%Y %H:%M})"


class MailingAttempt(models.Model):
    """
    Модель попытки отправки рассылки.

    Attributes:
        attempt_time (DateTimeField): Дата и время попытки.
        status (CharField): Статус попытки (Успешно / Не успешно).
        server_response (TextField): Ответ почтового сервера.
        mailing (ForeignKey): Рассылка, к которой относится попытка.
    """

    STATUS_SUCCESS = "Успешно"
    STATUS_FAILURE = "Не успешно"
    STATUS_CHOICES = [
        (STATUS_SUCCESS, "Успешно"),
        (STATUS_FAILURE, "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
    )
    server_response = models.TextField(blank=True, verbose_name="Ответ сервера")
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )

    class Meta:
        """Мета-параметры модели MailingAttempt."""

        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_time"]

    def __str__(self) -> str:
        """
        Возвращает строковое представление попытки.

        Returns:
            str: Статус и время попытки.
        """
        return f"{self.status} — {self.attempt_time:%d.%m.%Y %H:%M:%S}"