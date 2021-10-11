from django.contrib import admin
from .models import Group, Invite


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    pass
