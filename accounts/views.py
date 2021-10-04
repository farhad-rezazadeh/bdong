from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from config import settings
from accounts.forms import SignUpForm
from accounts.tokens import account_activation_token

User = get_user_model()


class LoginView(SuccessMessageMixin, LoginView):
    template_name = "registration/login.html"
    success_message = "login in successfully"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        return super(LoginView, self).get(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
        return super(RegisterView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activate your blog account."
        print(user, current_site.domain, account_activation_token.make_token(user))
        message = render_to_string(
            "registration/register_activate_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()
        message = "Please confirm your email address to complete the registration"
        return render(self.request, "registration/register_activate_complete.html", {"message": message})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        message = "Thank you for your email confirmation. Now you can login your account."
    else:
        message = "Activation link is invalid!"
    return render(request, "registration/register_activate_complete.html", {"message": message})


class PasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("account:password_reset_done")


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"


class AccountSettings(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = get_user_model()
    template_name = "dashboard/account/account_settings.html"
    fields = ["first_name", "last_name", "username", "email"]
    success_message = "fields changed successfully"
    success_url = reverse_lazy("account:account_settings")

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "dashboard/account/password_change.html"
    success_url = reverse_lazy("account:dashboard")
    success_message = "Password changed successfully"
