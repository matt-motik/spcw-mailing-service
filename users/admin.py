"""Настройки административной панели приложения users."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя в админке."""

    class Meta(UserCreationForm.Meta):
        """Мета-параметры формы."""

        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """Форма редактирования пользователя в админке."""

    class Meta(UserChangeForm.Meta):
        """Мета-параметры формы."""

        model = CustomUser
        fields = ("email",)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Настройки административной панели для модели CustomUser."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("email", "is_staff", "is_active", "country")
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные", {"fields": ("first_name", "last_name", "avatar", "country")}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        """
        Возвращает fieldsets в зависимости от режима (создание/редактирование).

        Args:
            request: HTTP-запрос.
            obj: Редактируемый объект или None при создании.

        Returns:
            tuple: Набор fieldsets для отображения.
        """
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)