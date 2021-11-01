from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from groups.models import Invite, Group


class DeleteInviteAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        invitation = get_object_or_404(Invite, pk=pk)
        if invitation in Invite.objects.get_all_user_invitations(request.user):
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class AcceptInviteAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        invitation = get_object_or_404(Invite, pk=pk)
        if invitation.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class CreatorGroupAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)
        if group.creator == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class LeaveGroupAccessMixin:
    def dispatch(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)
        if request.user in group.members.all() and request.user != group.creator:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()


class RemoveGroupMemberAccessMixin:
    def dispatch(self, request, group_pk, user_pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=group_pk)
        if group.creator == request.user and user_pk != request.user.pk:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
