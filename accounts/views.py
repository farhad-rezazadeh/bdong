from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages

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


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("account:login")
    success_message = "Please confirm your email address to complete the registration"

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
        message = render_to_string(
            "registration/register_activate_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "protocol": self.request.scheme,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = form.cleaned_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.content_subtype = "html"
        email.send()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)


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
        success = True
    else:
        message = "Activation link is invalid!"
        success = False
    return render(request, "registration/register_activate_complete.html", {"message": message, "success": success})


class PasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"
    html_email_template_name = "registration/password_reset_email.html"
    success_url = reverse_lazy("account:password_reset_done")


class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")
