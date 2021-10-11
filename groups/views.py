from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from groups.forms import GroupNameFrom, EmailForm
from groups.models import Group, Invite
from groups.mixins import DeleteInviteAccessMixin, AcceptInviteAccessMixin

User = get_user_model()


@login_required
def create_group(request):
    EmailFormset = formset_factory(EmailForm)

    if request.method == "POST":
        group_name_form = GroupNameFrom(request.POST, creator=request.user)
        email_formset = EmailFormset(request.POST)

        if group_name_form.is_valid() and email_formset.is_valid():
            group = Group.objects.create(name=group_name_form.cleaned_data["name"], creator=group_name_form.creator)
            group.members.add(request.user)
            for email_form in email_formset:
                if email_form.is_valid():
                    if member_email := email_form.cleaned_data.get("email"):
                        member = User.objects.get(email=member_email)
                        group.invite_member(member)
            messages.success(request, "Group created successfully")
            return HttpResponseRedirect(reverse("dashboard:dashboard"))
    else:
        group_name_form = GroupNameFrom(creator=request.user)
        email_formset = EmailFormset()

    context = {
        "group_name_form": group_name_form,
        "email_formset": email_formset,
    }

    return render(request, "dashboard/group/create_group.html", context)


class InviteListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/group/invite_list.html"

    def get_queryset(self):
        return Invite.objects.get_all_user_invitations(self.request.user)


class DeleteInviteView(LoginRequiredMixin, DeleteInviteAccessMixin, View):
    def get(self, request):
        invitation = get_object_or_404(Invite, pk=self.kwargs.get("pk"))
        invitation.delete()
        messages.success(request, "invitations successfully deleted")
        return HttpResponseRedirect(reverse("dashboard:group:invite_list"))


class AcceptInviteView(LoginRequiredMixin, AcceptInviteAccessMixin, View):
    def get(self, request):
        invitation = get_object_or_404(Invite, pk=self.kwargs.get("pk"))
        invitation.group.members.add(invitation.user)
        invitation.group.save()
        invitation.delete()
        messages.success(request, f"you join {invitation.group}")
        return HttpResponseRedirect(reverse("dashboard:group:invite_list"))
