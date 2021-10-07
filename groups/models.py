from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    members = models.ManyToManyField(User, related_name="expense_groups", related_query_name="expense_groups")
    created = models.DateTimeField(auto_now_add=True)
