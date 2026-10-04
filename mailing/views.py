"""Представления (views) приложения mailing."""

from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.db.models import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, MailingAttempt, Message, Recipient
from mailing.services import send_mailing, update_status


def is_manager(user: Any) -> bool:
    """Проверяет, что пользователь — менеджер или суперпользователь."""
    if user.is_superuser:
        return True
    return bool(user.groups.filter(name="Менеджер").exists())


class RecipientListView(LoginRequiredMixin, ListView):
    """Список получателей текущего пользователя."""

    model: type[Recipient] = Recipient
    template_name = "mailing/recipient_list.html"
    context_object_name = "recipients"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Recipient]:
        """Возвращает получателей: все для менеджера, свои для остальных."""
        queryset = Recipient.objects.all()
        if is_manager(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    """Детали получателя."""

    model: type[Recipient] = Recipient
    template_name = "mailing/recipient_detail.html"
    context_object_name = "recipient"

    def get_queryset(self) -> QuerySet[Recipient]:
        """Возвращает получателей: все для менеджера, свои для остальных."""
        queryset = Recipient.objects.all()
        if is_manager(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)


class RecipientCreateView(LoginRequiredMixin, CreateView):
    """Добавление получателя."""

    model: type[Recipient] = Recipient
    form_class: type[RecipientForm] = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url: str = reverse_lazy("mailing:recipient_list")

    def form_valid(self, form: RecipientForm) -> HttpResponse:
        """Назначает владельца и сохраняет получателя."""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Получатель '{self.object.full_name}' добавлен.", extra_tags="mailing")
        return response


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование получателя."""

    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self) -> QuerySet[Recipient]:
        """Редактировать можно своих, суперпользователь — любых."""
        if self.request.user.is_superuser:
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)

    def form_valid(self, form: RecipientForm) -> HttpResponse:
        """Сохраняет изменения и выводит сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, f"Получатель '{self.object.full_name}' обновлён.", extra_tags="mailing")
        return response


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление получателя."""

    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_queryset(self) -> QuerySet[Recipient]:
        """Удалять можно своих, суперпользователь — любых."""
        if self.request.user.is_superuser:
            return Recipient.objects.all()
        return Recipient.objects.filter(owner=self.request.user)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Удаляет получателя и выводит сообщение об успехе."""
        name = self.object.full_name
        response = super().form_valid(form)
        messages.success(self.request, f"Получатель '{name}' удалён.", extra_tags="mailing")
        return response


class MessageListView(LoginRequiredMixin, ListView):
    """Список сообщений."""

    model = Message
    template_name = "mailing/message_list.html"
    context_object_name = "messages"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Message]:
        """Возвращает сообщения: все для менеджера, свои для остальных."""
        queryset = Message.objects.all()
        if is_manager(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Детали сообщения."""

    model = Message
    template_name = "mailing/message_detail.html"
    context_object_name = "message"

    def get_queryset(self) -> QuerySet[Message]:
        """Возвращает сообщения: все для менеджера, свои для остальных."""
        queryset = Message.objects.all()
        if is_manager(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Добавление сообщения."""

    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def form_valid(self, form: MessageForm) -> HttpResponse:
        """Назначает владельца и сохраняет сообщение."""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Сообщение '{self.object.subject}' добавлено.", extra_tags="mailing")
        return response


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения."""

    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self) -> QuerySet[Message]:
        """Редактировать можно свои, суперпользователь — любые."""
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def form_valid(self, form: MessageForm) -> HttpResponse:
        """Сохраняет изменения и выводит сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, f"Сообщение '{self.object.subject}' обновлено.", extra_tags="mailing")
        return response


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения."""

    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_queryset(self) -> QuerySet[Message]:
        """Удалять можно свои, суперпользователь — любые."""
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Удаляет сообщение и выводит сообщение об успехе."""
        subject = self.object.subject
        response = super().form_valid(form)
        messages.success(self.request, f"Сообщение '{subject}' удалено.", extra_tags="mailing")
        return response


class MailingListView(LoginRequiredMixin, ListView):
    """Список рассылок."""

    model = Mailing
    template_name = "mailing/mailing_list.html"
    context_object_name = "mailings"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Mailing]:
        """Возвращает рассылки: все для менеджера, свои для остальных."""
        queryset = Mailing.objects.select_related("message", "owner")
        if is_manager(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    """Детали рассылки с пересчётом статуса."""

    model = Mailing
    template_name = "mailing/mailing_detail.html"
    context_object_name = "mailing"

    def get_queryset(self) -> QuerySet[Mailing]:
        """Возвращает рассылки: все для менеджера, свои для остальных."""
        queryset = Mailing.objects.select_related("message", "owner")
        if is_manager(self.request.user):
            return queryset
        return queryset.filter(owner=self.request.user)

    def get_object(self, queryset: QuerySet[Mailing] | None = None) -> Mailing:
        """Возвращает рассылку с обновлённым статусом."""
        obj: Mailing = super().get_object(queryset)
        update_status(obj)
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    """Добавление рассылки."""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form: MailingForm) -> HttpResponse:
        """Назначает владельца и сохраняет рассылку."""
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Рассылка создана.", extra_tags="mailing")
        return response


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование рассылки."""

    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self) -> QuerySet[Mailing]:
        """Редактировать можно свои, суперпользователь — любые."""
        if self.request.user.is_superuser:
            return Mailing.objects.select_related("message", "owner")
        return Mailing.objects.select_related("message", "owner").filter(owner=self.request.user)

    def form_valid(self, form: MailingForm) -> HttpResponse:
        """Сохраняет изменения и выводит сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, "Рассылка обновлена.", extra_tags="mailing")
        return response


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки."""

    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_queryset(self) -> QuerySet[Mailing]:
        """Удалять можно свои, суперпользователь — любые."""
        if self.request.user.is_superuser:
            return Mailing.objects.select_related("message", "owner")
        return Mailing.objects.select_related("message", "owner").filter(owner=self.request.user)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Удаляет рассылку и выводит сообщение об успехе."""
        response = super().form_valid(form)
        messages.success(self.request, "Рассылка удалена.", extra_tags="mailing")
        return response


class MailingSendView(LoginRequiredMixin, View):
    """Ручной запуск рассылки."""

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Отправляет рассылку и показывает результат."""
        queryset = Mailing.objects.all() if request.user.is_superuser else Mailing.objects.filter(owner=request.user)
        mailing = get_object_or_404(queryset, pk=pk)

        try:
            success, failure = send_mailing(mailing)
        except ValueError as exc:
            messages.error(request, str(exc), extra_tags="mailing")
        else:
            messages.success(
                request,
                f"Рассылка отправлена. Успешно: {success}, неудачно: {failure}.",
                extra_tags="mailing",
            )
        return redirect("mailing:mailing_detail", pk=mailing.pk)


@method_decorator(cache_control(public=True, max_age=60), name="dispatch")
class IndexView(TemplateView):
    """Главная страница со статистикой.

    Агрегаты кешируются в Redis на 15 минут, браузер — на 60 секунд.
    Доступна анонимам.
    """

    template_name = "mailing/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Добавляет агрегаты в контекст (из кеша или БД)."""
        context: dict[str, Any] = super().get_context_data(**kwargs)
        stats = cache.get("index_stats")
        if stats is None:
            now = timezone.now()
            stats = {
                "total_mailings": Mailing.objects.count(),
                "active_mailings": Mailing.objects.filter(
                    start_time__lte=now,
                    end_time__gte=now,
                    status=Mailing.STATUS_STARTED,
                ).count(),
                "unique_recipients": Recipient.objects.count(),
            }
            cache.set("index_stats", stats, timeout=60 * 15)
        context.update(stats)
        return context


class MailingDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Отключение рассылки менеджером."""

    permission_required = "mailing.can_disable_mailing"

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Отключает рассылку."""
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_disabled = True
        mailing.save(update_fields=["is_disabled", "updated_at"])
        messages.success(request, "Рассылка отключена.", extra_tags="mailing")
        return redirect("mailing:mailing_detail", pk=mailing.pk)


class MailingEnableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Включение рассылки менеджером."""

    permission_required = "mailing.can_disable_mailing"

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Снимает флаг отключения."""
        mailing = get_object_or_404(Mailing, pk=pk)
        mailing.is_disabled = False
        mailing.save(update_fields=["is_disabled", "updated_at"])
        messages.success(request, "Рассылка включена.", extra_tags="mailing")
        return redirect("mailing:mailing_detail", pk=mailing.pk)


@method_decorator(cache_control(private=True, max_age=0), name="dispatch")
class StatisticsView(LoginRequiredMixin, TemplateView):
    """Статистика по попыткам рассылок текущего пользователя.

    Агрегаты кешируются в Redis на 15 минут по ключу stats:user:{id}.
    Для менеджера и суперпользователя кеш не используется.
    """

    template_name = "mailing/statistics.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Собирает агрегаты по попыткам (из кеша или БД)."""
        context: dict[str, Any] = super().get_context_data(**kwargs)
        user = self.request.user

        mailings = Mailing.objects.all()
        if not (user.is_superuser or is_manager(user)):
            mailings = mailings.filter(owner=user)

        cache_key = f"stats:user:{user.pk}"
        stats = None
        if not (user.is_superuser or is_manager(user)):
            stats = cache.get(cache_key)

        if stats is None:
            attempts = MailingAttempt.objects.filter(mailing__in=mailings)
            stats = {
                "total_attempts": attempts.count(),
                "success_attempts": attempts.filter(status=MailingAttempt.STATUS_SUCCESS).count(),
                "failure_attempts": attempts.filter(status=MailingAttempt.STATUS_FAILURE).count(),
            }
            if not (user.is_superuser or is_manager(user)):
                cache.set(cache_key, stats, timeout=60 * 15)

        context.update(stats)
        context["mailings"] = mailings.order_by("-created_at")
        return context
