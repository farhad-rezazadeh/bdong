from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, View
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage

from dashboard.utils import get_balance, get_total_debt, get_total_credit
from expenses.models import Share
from groups.models import Invite

User = get_user_model()


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["balance"] = get_balance(self.request.user)
        context["credit"] = get_total_credit(self.request.user)
        context["debt"] = get_total_debt(self.request.user)
        context["spent"] = Share.objects.get_spent(self.request.user)
        context["share_per_group"] = Share.objects.get_group_most_share(self.request.user)
        context["invitations"] = Invite.objects.get_all_user_invitations(self.request.user).count()
        return context


class InviteFriendView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        current_site = get_current_site(self.request)
        mail_subject = "Activate your blog account."
        message = render_to_string(
            "dashboard/invite_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "protocol": self.request.scheme,
            },
        )
        to_email = request.POST.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()
        messages.success(self.request, "an email sent to invite email.")
        return HttpResponseRedirect(reverse("dashboard:dashboard"))


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
