from decimal import Decimal

from django.db import models
from django.db.models import Q, F, Sum
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from groups.models import Group

User = get_user_model()


class ExpenseManager(models.Manager):
    def create_expense(self, data, creator):
        expense = self.create(
            description=data["description"],
            creator=creator,
            group=Group.objects.get(pk=data["group_pk"]),
            total_cost=Decimal(data["total_cost"]).quantize(Decimal(".00")),
        )
        for participant in data["participants"]:
            user = User.objects.get(email=participant[0])
            expense.participants.add(
                user,
                through_defaults={
                    "share": Decimal(participant[1]).quantize(Decimal(".00")),
                    "paid": Decimal(participant[2]).quantize(Decimal(".00")),
                },
            )
        return expense


# Create your models here.
class Expense(models.Model):
    description = models.TextField()
    participants = models.ManyToManyField(
        User, through="Share", related_name="participants", related_query_name="participants"
    )
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(
        default=0.00, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )

    objects = ExpenseManager()

    def get_debtors(self):
        return Share.objects.filter(expense=self, paid__lt=F("share")).order_by("user").values("user", "share", "paid")

    def get_creditors(self):
        return Share.objects.filter(expense=self, paid__gt=F("share")).order_by("user").values("user", "share", "paid")

    def get_totoal_transfer_amount(self):
        debtors = self.get_debtors()
        return sum([debtor["share"] - debtor["paid"] for debtor in debtors])

    def __str__(self):
        return self.description


class ShareManger(models.Manager):
    def get_spent(self, user):
        return self.filter(user=user).aggregate(Sum("share"))["share__sum"] or 0

    def get_group_most_share(self, user):
        expense_per_group = self.filter(user=user).values("expense__group").annotate(Sum("share"))
        expense_per_group = [
            (str(Group.objects.get(pk=_["expense__group"])), float(_["share__sum"])) for _ in expense_per_group
        ][:4]
        sum_expense_per_group = sum([_[1] for _ in expense_per_group])
        expense_per_group.append(("other", float(self.get_spent(user)) - sum_expense_per_group))
        return expense_per_group


class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    share = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    paid = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])

    objects = ShareManger()

    class Meta:
        unique_together = [["user", "expense"]]
