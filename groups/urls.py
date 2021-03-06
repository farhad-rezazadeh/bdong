from django.urls import path

from groups.views import (
    create_group,
    InviteListView,
    DeleteInviteView,
    AcceptInviteView,
    GroupListView,
    DeleteGroupView,
    LeaveGroupView,
    RemoveGroupMemberView,
    InviteMemberView,
    ChangeGroupName,
)

app_name = "group"

urlpatterns = [
    path("create/", create_group, name="create_group"),
    path("invite_list/", InviteListView.as_view(), name="invite_list"),
    path("delete_invite/<int:pk>/", DeleteInviteView.as_view(), name="delete_invite"),
    path("accept_invite/<int:pk>/", AcceptInviteView.as_view(), name="accept_invite"),
    path("group_list", GroupListView.as_view(), name="group_list"),
    path("delete_group/<int:pk>/", DeleteGroupView.as_view(), name="delete_group"),
    path("leave_group/<int:pk>/", LeaveGroupView.as_view(), name="leave_group"),
    path(
        "remover_group_member/<int:group_pk>/<int:user_pk>/",
        RemoveGroupMemberView.as_view(),
        name="remove_group_member",
    ),
    path("invite_member/<int:pk>/", InviteMemberView.as_view(), name="invite_member"),
    path("change_group_name/<int:pk>/", ChangeGroupName.as_view(), name="change_group_name"),
]
