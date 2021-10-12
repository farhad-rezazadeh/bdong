from django.urls import path

from groups.views import create_group, InviteListView, DeleteInviteView, AcceptInviteView, GroupListView

app_name = "group"

urlpatterns = [
    path("create/", create_group, name="create_group"),
    path("invite_list/", InviteListView.as_view(), name="invite_list"),
    path("delete_invite/<int:pk>/", DeleteInviteView.as_view(), name="delete_invite"),
    path("accept_invite/<int:pk>/", AcceptInviteView.as_view(), name="accept_invite"),
    path("group_list", GroupListView.as_view(), name="group_list"),
]
