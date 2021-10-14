from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from django.contrib import messages
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from groups.forms import GroupNameFrom, EmailForm
from groups.models import Group, Invite
from groups.mixins import (
    DeleteInviteAccessMixin,
    AcceptInviteAccessMixin,
    DeleteGroupAccessMixin,
    RemoveGroupMemberAccessMixin,
    LeaveGroupAccessMixin,
)

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


class GroupListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/group/group_list.html"

    def get_queryset(self):
        user = self.request.user
        return user.expense_groups.all()

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context["form"] = EmailForm()
        return context


class DeleteGroupView(LoginRequiredMixin, DeleteGroupAccessMixin, View):
    def get(self, request):
        group = get_object_or_404(Group, pk=self.kwargs.get("pk"))
        group.delete()
        messages.success(request, "group successfully deleted")
        return HttpResponseRedirect(reverse("dashboard:group:group_list"))


class LeaveGroupView(LoginRequiredMixin, LeaveGroupAccessMixin, View):
    def get(self, request):
        group = get_object_or_404(Group, pk=self.kwargs.get("pk"))
        group.members.remove(request.user)
        messages.success(request, "you leave group")
        return HttpResponseRedirect(reverse("dashboard:group:group_list"))


class RemoveGroupMemberView(LoginRequiredMixin, RemoveGroupMemberAccessMixin, View):
    def get(self, request):
        group = get_object_or_404(Group, pk=self.kwargs.get("group_pk"))
        user = get_object_or_404(User, pk=self.kwargs.get("user_pk"))
        group.members.remove(user)
        messages.success(request, "memeber removed")
        return HttpResponseRedirect(reverse("dashboard:group:group_list"))


class ManageGroupView(View):
    EmailFormset = formset_factory(EmailForm)

    def get(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        group_name_form = GroupNameFrom(creator=request.user, group=group, initial={"name": group.name})
        email_formset = self.EmailFormset()
        context = {"group_name_form": group_name_form, "email_formset": email_formset, "group_pk": pk}
        return render(request, "dashboard/group/manage_modal.html", context=context)

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        group_name_form = GroupNameFrom(request.POST, creator=request.user, group=group)
        email_formset = self.EmailFormset(request.POST)

        if group_name_form.is_valid() and email_formset.is_valid():
            group.name = group_name_form.cleaned_data["name"]
            for email_form in email_formset:
                if email_form.is_valid():
                    if member_email := email_form.cleaned_data.get("email"):
                        member = User.objects.get(email=member_email)
                        group.invite_member(member)
            group.save()
            return HttpResponse(
                """
                    <div class="alert alert-success mb-2" role="alert">
                    change and invite successfully take place
                    </div>
                    <div class="float-right">
                    <button type="button" class="btn btn-warning glow mr-sm-1 mb-1" onclick="closeModal()">Close</button>
                    </div>
                    """
            )
        if request.htmx:
            context = {"group_name_form": group_name_form, "email_formset": email_formset, "group_pk": pk}
            return render(request, "dashboard/group/mange_form.html", context=context)
