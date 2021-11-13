from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from groups.models import Group

User = get_user_model()


class AddExpenseAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            participants = request.session["add_expense"]["participants"]
            total_cost = request.session["add_expense"]["total_cost"]
            assert total_cost >= 0
            description = request.session["add_expense"]["description"]
            group = get_object_or_404(Group, pk=request.session["add_expense"]["group_pk"])
            all_participant_is_group_member = all(
                [User.objects.get(email=participant[0]) in group.members.all() for participant in participants]
            )
            paid_sum = 0
            share_sum = 0
            for participant in participants:
                assert participant[1] >= 0 and participant[2] >= 0
                share_sum += participant[1]
                paid_sum += participant[2]

            if (
                request.user in group.members.all()
                and all_participant_is_group_member
                and paid_sum == total_cost
                and share_sum == total_cost
            ):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()
        except:
            return Http404()
