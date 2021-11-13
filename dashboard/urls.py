from django.urls import path, include

from dashboard.views import (
    Dashboard,
    PasswordChangeView,
    AccountSettings,
)

app_name = "dashboard"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("settings/general/", AccountSettings.as_view(), name="account_settings"),
    path("settings/password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("group/", include("groups.urls")),
    path("wallet/", include("wallet.urls")),
    path("expense/", include("expenses.urls")),
]
