"""URL-маршрутизация приложения users."""

from django.urls import path

from .views import (
    ActivateView,
    ActivationSentView,
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetCompleteView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    CustomPasswordResetView,
    ProfileDetailView,
    ProfileUpdateView,
    RegisterView,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activation-sent/", ActivationSentView.as_view(), name="activation_sent"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("password/change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "password/reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/reset/complete/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
