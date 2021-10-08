from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.forms import formset_factory
from django.contrib import messages
from django.urls import reverse

from .forms import GroupNameFrom, EmailForm
from .models import Group

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
                        group.members.add(member)
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
