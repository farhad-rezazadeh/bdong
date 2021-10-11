from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from groups.models import Invite


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
