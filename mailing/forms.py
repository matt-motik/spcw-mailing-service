"""Формы приложения mailing."""

from django import forms

from config.mixins import BootstrapStyleMixin
from django.utils import timezone

from mailing.models import Mailing, Message, Recipient


class RecipientForm(BootstrapStyleMixin, forms.ModelForm):
    """Форма создания и редактирования получателя."""

    class Meta:
        """Мета-параметры формы."""

        model = Recipient
        fields = ("email", "full_name", "comment")
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "full_name": forms.TextInput(attrs={"placeholder": "Иванов Иван Иванович"}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Заметка о получателе"}),
        }

class MessageForm(BootstrapStyleMixin, forms.ModelForm):
    """Форма создания и редактирования сообщения."""

    class Meta:
        """Мета-параметры формы."""

        model = Message
        fields = ("subject", "body")
        widgets = {
            "subject": forms.TextInput(attrs={"placeholder": "Тема письма"}),
            "body": forms.Textarea(attrs={"rows": 8, "placeholder": "Текст письма"}),
        }

class MailingForm(BootstrapStyleMixin, forms.ModelForm):
    """Форма создания и редактирования рассылки с валидацией дат."""

    class Meta:
        """Мета-параметры формы."""

        model = Mailing
        fields = ("start_time", "end_time", "message", "recipients")
        widgets = {
            "start_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "recipients": forms.SelectMultiple(attrs={"size": 10}),
        }

    def __init__(self, *args, **kwargs):
        """Настраивает формат ввода дат для datetime-local."""
        super().__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["end_time"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_start_time(self):
        """Проверяет, что start_time не в прошлом."""
        start_time = self.cleaned_data["start_time"]
        if start_time < timezone.now():
            raise forms.ValidationError("Дата начала не может быть в прошлом.")
        return start_time

    def clean(self):
        """Проверяет, что start_time раньше end_time."""
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Дата начала должна быть раньше даты окончания.")
        return cleaned_data