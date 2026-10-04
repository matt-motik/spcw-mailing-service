"""Представления (views) приложения users."""

import smtplib
from typing import cast

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, FormView, UpdateView

from users.forms import (
    CustomAuthenticationForm,
    CustomPasswordChangeForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
)
from users.models import CustomUser


class RegisterView(FormView):
    """Регистрация нового пользователя.

    Создаёт неактивного пользователя (is_active=False) и отправляет
    письмо со ссылкой для активации. Автоматический вход не выполняется:
    пользователь должен сначала подтвердить email.
    """

    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:activation_sent")

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        """Сохраняет пользователя и отправляет письмо с токеном активации.

        Если письмо не удалось отправить, пользователь удаляется,
        а на страницу регистрации выводится сообщение об ошибке.

        Args:
            form: Валидная форма регистрации.

        Returns:
            HttpResponse: Редирект на страницу «проверьте почту» или обратно на регистрацию.
        """
        user: CustomUser = form.save(commit=False)
        user.is_active = False
        user.save()

        try:
            self.send_activation_email(user)
        except smtplib.SMTPException, OSError:
            user.delete()
            messages.error(
                self.request,
                "Не удалось отправить письмо с активацией. Попробуйте зарегистрироваться позже.",
                extra_tags="users",
            )
            return redirect("users:register")

        messages.success(
            self.request,
            "Регистрация прошла успешно. Проверьте почту и подтвердите аккаунт.",
            extra_tags="users",
        )
        return super().form_valid(form)

    def send_activation_email(self, user: CustomUser) -> None:
        """Отправляет письмо со ссылкой активации.

        Args:
            user: Только что созданный неактивный пользователь.

        Raises:
            smtplib.SMTPException: Если отправка письма не удалась.
            OSError: Если почтовый сервер недоступен.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_path = reverse(
            "users:activate",
            kwargs={"uidb64": uidb64, "token": token},
        )
        activation_url = self.request.build_absolute_uri(activation_path)

        subject = "Подтверждение регистрации"
        message = (
            f"Здравствуйте, {user.first_name or user.email}!\n\n"
            f"Для активации аккаунта перейдите по ссылке:\n{activation_url}\n\n"
            f"Ссылка действует {settings.PASSWORD_RESET_TIMEOUT // 3600} ч."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


class ActivationSentView(View):
    """Страница «проверьте почту» после регистрации."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Отображает страницу с инструкцией.

        Args:
            request: HTTP-запрос.

        Returns:
            HttpResponse: Страница activation_sent.html.
        """
        return render(request, "users/activation_sent.html")


class ActivateView(View):
    """Активация аккаунта по ссылке из письма.

    Принимает uidb64 и token, проверяет их и, если всё корректно,
    устанавливает is_active=True.
    """

    def get(self, request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
        """Обрабатывает переход по ссылке активации.

        Args:
            request: HTTP-запрос.
            uidb64: Закодированный в base64 первичный ключ пользователя.
            token: Токен активации.

        Returns:
            HttpResponse: Редирект на логин при успехе или страница ошибки.
        """
        user = self._get_user(uidb64)

        if user is None or not default_token_generator.check_token(user, token):
            return render(request, "users/activation_invalid.html", status=400)

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        messages.success(
            request,
            "Аккаунт активирован. Теперь можно войти.",
            extra_tags="users",
        )
        return redirect("users:login")

    @staticmethod
    def _get_user(uidb64: str) -> CustomUser | None:
        """Декодирует uidb64 и возвращает пользователя.

        Args:
            uidb64: Закодированный первичный ключ пользователя.

        Returns:
            CustomUser | None: Пользователь или None, если декодирование не удалось.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user: CustomUser = CustomUser.objects.get(pk=uid)
            return user
        except TypeError, ValueError, OverflowError, CustomUser.DoesNotExist:
            return None


class CustomLoginView(LoginView):
    """Авторизация пользователя по email и паролю.

    Использует CustomAuthenticationForm с понятным сообщением для
    неактивного пользователя.
    """

    template_name = "users/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    """Выход пользователя из системы."""

    next_page = reverse_lazy("users:login")


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Просмотр профиля текущего пользователя.

    Доступно только авторизованным. Показывает данные пользователя
    и кнопки перехода к редактированию и смене пароля.
    """

    model: type[CustomUser] = CustomUser
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self, queryset: QuerySet[CustomUser] | None = None) -> CustomUser:
        """Возвращает текущего пользователя.

        Args:
            queryset: Не используется, оставлен для совместимости с DetailView.

        Returns:
            CustomUser: Текущий авторизованный пользователь.
        """
        return cast(CustomUser, self.request.user)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля текущего пользователя.

    Доступно только авторизованным. После сохранения возвращает на
    страницу просмотра профиля и выводит сообщение об успехе.
    """

    model: type[CustomUser] = CustomUser
    form_class: type[CustomUserChangeForm] = CustomUserChangeForm
    template_name = "users/profile_form.html"
    success_url: str = reverse_lazy("users:profile")

    def get_object(self, queryset: QuerySet[CustomUser] | None = None) -> CustomUser:
        """Возвращает текущего пользователя.

        Args:
            queryset: Не используется, оставлен для совместимости с UpdateView.

        Returns:
            CustomUser: Текущий авторизованный пользователь.
        """
        return cast(CustomUser, self.request.user)

    def form_valid(self, form: CustomUserChangeForm) -> HttpResponse:
        """Сохраняет профиль и добавляет сообщение об успехе.

        Args:
            form: Валидная форма редактирования профиля.

        Returns:
            HttpResponse: Ответ после успешного сохранения.
        """
        response = super().form_valid(form)
        messages.success(self.request, "Профиль успешно обновлён!", extra_tags="users")
        return response


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Смена пароля текущего пользователя.

    Доступно только авторизованным. После успешной смены пароля
    возвращает на страницу профиля и выводит сообщение об успехе.
    """

    form_class: type[CustomPasswordChangeForm] = CustomPasswordChangeForm
    template_name = "users/password_change.html"
    success_url: str = reverse_lazy("users:profile")

    def form_valid(self, form: CustomPasswordChangeForm) -> HttpResponse:
        """Сохраняет новый пароль и добавляет сообщение об успехе.

        Args:
            form: Валидная форма смены пароля.

        Returns:
            HttpResponse: Ответ после успешного сохранения.
        """
        response = super().form_valid(form)
        messages.success(self.request, "Пароль успешно изменён!", extra_tags="users")
        return response


class CustomPasswordResetView(PasswordResetView):
    """Запрос на восстановление пароля.

    Принимает email, отправляет письмо со ссылкой для сброса пароля.
    Всегда показывает страницу «письмо отправлено», даже если email
    не зарегистрирован — чтобы не раскрывать базу пользователей.
    """

    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Страница «письмо отправлено» после запроса на сброс пароля."""

    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Установка нового пароля по ссылке из письма."""

    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Страница «пароль изменён» после успешного сброса."""

    template_name = "users/password_reset_complete.html"
