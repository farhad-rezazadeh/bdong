from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"


class AccountSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    template_name = "dashboard/account/account_settings.html"
    fields = ["first_name", "last_name", "username", "email"]
    success_message = "fields changed successfully"
    success_url = reverse_lazy("dashboard:account_settings")

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "dashboard/account/password_change.html"
    success_url = reverse_lazy("dashboard:dashboard")
    success_message = "Password changed successfully"
