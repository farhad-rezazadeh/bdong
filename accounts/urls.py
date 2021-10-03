from django.urls import path, include
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, LogoutView

from accounts.views import LoginView, RegisterView, activate, PasswordResetView, PasswordResetConfirmView, dashboard

app_name = "account"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", include("social_django.urls", namespace="social")),
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("dashboard/", dashboard, name="dashboard"),
]
