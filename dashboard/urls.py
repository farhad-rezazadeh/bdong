from django.urls import path, include

from dashboard.views import (
    Dashboard,
    InviteFriendView,
    PasswordChangeView,
    AccountSettings,
)

app_name = "dashboard"

urlpatterns = [
    path("", Dashboard.as_view(), name="dashboard"),
    path("invite_friend", InviteFriendView.as_view(), name="invite_friend"),
    path("settings/general/", AccountSettings.as_view(), name="account_settings"),
    path("settings/password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("group/", include("groups.urls")),
    path("wallet/", include("wallet.urls")),
    path("expense/", include("expenses.urls")),
]
