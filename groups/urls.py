from django.urls import path

from groups.views import create_group

app_name = "group"

urlpatterns = [
    path("create/", create_group, name="create_group"),
]
