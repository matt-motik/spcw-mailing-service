"""Формы приложения users."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, UserCreationForm
from django.core.exceptions import ValidationError

from config.mixins import BootstrapStyleMixin
from users.models import CustomUser


class CustomUserCreationForm(BootstrapStyleMixin, UserCreationForm):
    """Форма регистрации нового пользователя.

    Использует email вместо username. Включает встроенные поля password1
    и password2 (пароль и его подтверждение) из UserCreationForm.

    Attributes:
        Meta: Внутренний класс с настройками формы.
    """

    class Meta(UserCreationForm.Meta):
        """
        Внутренний класс с настройками формы.

        Attributes:
            model (Model): Модель, с которой связана форма.
            fields (tuple): Список полей, включённых в форму.
            widgets (dict): Словарь с настройками виджетов для полей.
        """

        model = CustomUser
        fields = ("email", "first_name", "last_name")
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "you@example.com",
                    "autocomplete": "email",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Иван",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Иванов",
                    "autocomplete": "family-name",
                }
            ),
        }

    def clean_email(self) -> str:
        """Проверяет, что email ещё не занят.

        Returns:
            str: Email в нижнем регистре.

        Raises:
            ValidationError: Если пользователь с таким email уже существует.
        """
        email: str = self.cleaned_data.get("email", "").lower()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email


class CustomAuthenticationForm(BootstrapStyleMixin, AuthenticationForm):
    """Форма авторизации по email и паролю.

    Переопределяет стандартную AuthenticationForm: поле username
    переименовано в email для отображения в шаблоне.
    """

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "autofocus": True,
            }
        ),
    )


class CustomUserChangeForm(BootstrapStyleMixin, forms.ModelForm):
    """Форма редактирования профиля пользователя.

    Позволяет изменить имя, фамилию, страну и аватар.
    Email и пароль через эту форму не редактируются.

    Attributes:
        Meta: Внутренний класс с настройками формы.
    """

    class Meta:
        """
        Внутренний класс с настройками формы.

        Attributes:
            model (Model): Модель, с которой связана форма.
            fields (tuple): Список полей, доступных для редактирования.
            widgets (dict): Словарь с настройками виджетов для полей.
        """

        model = CustomUser
        fields = ("first_name", "last_name", "country", "avatar")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "Иван",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Иванов",
                    "autocomplete": "family-name",
                }
            ),
            "country": forms.TextInput(
                attrs={
                    "placeholder": "Россия",
                    "autocomplete": "country-name",
                }
            ),
            "avatar": forms.FileInput(
                attrs={
                    "accept": "image/jpeg,image/jpg,image/png,image/webp",
                }
            ),
        }


class CustomPasswordChangeForm(BootstrapStyleMixin, PasswordChangeForm):
    """Форма смены пароля с Bootstrap-стилями.

    Наследуется от стандартной PasswordChangeForm, которая уже содержит
    поля old_password, new_password1 и new_password2 с валидацией.
    """


class CustomPasswordResetForm(BootstrapStyleMixin, PasswordResetForm):
    """Форма запроса восстановления пароля с Bootstrap-стилями."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "class": "form-control",
            }
        ),
    )
