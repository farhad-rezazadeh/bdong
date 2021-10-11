from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class InviteManager(models.Manager):
    def get_all_user_invitations(self, user):
        return self.filter(Q(caller=user) | Q(user=user))


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name="expense_groups", related_query_name="expense_groups")
    created = models.DateTimeField(auto_now_add=True)

    def invite_member(self, user):
        return Invite.objects.create(group=self, caller=self.creator, user=user)

    def __str__(self):
        return f"{self.name} #{self.id}"


class Invite(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    caller = models.ForeignKey(User, related_name="caller", related_query_name="caller", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invite_date = models.DateTimeField(auto_now_add=True)

    objects = InviteManager()
