from decimal import Decimal

from django.shortcuts import render
from django.views.generic import View, ListView
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, reverse

from groups.models import Group
from expenses.forms import AddExpenseFromStep1, AddExpenseFromStep2
from expenses.models import Expense
from expenses.utils import insert_data
from expenses.mixins import AddExpenseAccessMixin


class CreateExpenseView(LoginRequiredMixin, View):
    add_expense_step2_formset = formset_factory(AddExpenseFromStep2, extra=0)

    def get(self, request, step="1"):
        if step == "1":
            if request.htmx:
                initial = {
                    "total_cost": Decimal(request.session["add_expense"]["total_cost"]).quantize(Decimal(".00")),
                    "group": Group.objects.get(pk=request.session["add_expense"]["group_pk"]),
                    "description": request.session["add_expense"]["description"],
                }
                form = AddExpenseFromStep1(initial=initial, user=request.user)
                return render(request, "dashboard/expense/add_expense_step1_form.html", {"form": form})
            request.session["add_expense"] = {}
            form = AddExpenseFromStep1(user=request.user)
            return render(request, "dashboard/expense/add_expense_base.html", {"form": form})
        if step == "2":
            if request.htmx:
                initial = [
                    {
                        "user": data[0],
                        "share": Decimal(data[1]).quantize(Decimal(".00")),
                        "paid": Decimal(data[2]).quantize(Decimal(".00")),
                    }
                    for data in request.session["add_expense"]["participants"]
                ]
                forms = self.add_expense_step2_formset(initial=initial)
                return render(request, "dashboard/expense/add_expense_step2_form.html", {"forms": forms})

    def post(self, request, step):
        if step == "2":
            if request.htmx:
                form = AddExpenseFromStep1(request.POST, user=request.user)
                if form.is_valid():
                    group = form.cleaned_data["group"]

                    request.session["add_expense"]["total_cost"] = float(form.cleaned_data["total_cost"])
                    request.session["add_expense"]["group_pk"] = group.pk
                    request.session["add_expense"]["description"] = form.cleaned_data["description"]

                    request.session.modified = True

                    if request.session["add_expense"].get("participants"):
                        initial = [
                            {
                                "user": data[0],
                                "share": Decimal(data[1]).quantize(Decimal(".00")),
                                "paid": Decimal(data[2]).quantize(Decimal(".00")),
                            }
                            for data in request.session["add_expense"]["participants"]
                        ]
                    else:

                        initial = [{"user": user.email, "share": 0, "paid": 0} for user in group.members.all()]

                    forms = self.add_expense_step2_formset(initial=initial)
                    return render(request, "dashboard/expense/add_expense_step2_form.html", {"forms": forms})
                else:
                    return render(request, "dashboard/expense/add_expense_step1_form.html", {"form": form})

        if step == "3":
            if request.htmx:
                forms = self.add_expense_step2_formset(request.POST)
                if forms.is_valid():
                    paid_sum = 0
                    share_sum = 0
                    for form in forms:
                        if form.is_valid():
                            paid_sum += float(form.cleaned_data["paid"])
                            share_sum += float(form.cleaned_data["share"])
                        else:
                            return render(request, "dashboard/expense/add_expense_step2_form.html", {"forms": forms})

                    if (
                        abs(paid_sum - request.session["add_expense"]["total_cost"]) > 0.00001
                        or abs(share_sum - request.session["add_expense"]["total_cost"]) > 0.00001
                    ):
                        error = f'Sum of paid or sum of share is not equal to total cost \n your total cost is {request.session["add_expense"]["total_cost"]}'
                        return render(
                            request, "dashboard/expense/add_expense_step2_form.html", {"forms": forms, "error": error}
                        )
                    else:
                        request.session["add_expense"]["participants"] = []
                        for form in forms:
                            request.session["add_expense"]["participants"].append(
                                [
                                    form.cleaned_data["user"],
                                    float(form.cleaned_data["share"]),
                                    float(form.cleaned_data["paid"]),
                                ]
                            )
                        request.session.modified = True
                        group = Group.objects.get(pk=request.session["add_expense"]["group_pk"])
                        return render(request, "dashboard/expense/add_expense_step3.html", {"group": group})
                return render(request, "dashboard/expense/add_expense_step2_form.html", {"forms": forms})


class HTTPResponseHXRedirect(HttpResponseRedirect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self["HX-Redirect"] = self["Location"]

    status_code = 200


class SubmitExpense(LoginRequiredMixin, AddExpenseAccessMixin, View):
    def get(self, request):
        expense = Expense.objects.create_expense(request.session["add_expense"], creator=request.user)
        total_transfer_amount = expense.get_totoal_transfer_amount()
        for creditor in expense.get_creditors():
            for debtor in expense.get_debtors():
                insert_data(creditor, debtor, total_transfer_amount)
        request.session["add_expense"] = None
        messages.success(request, "Expense added")
        return HTTPResponseHXRedirect(redirect_to=reverse_lazy("dashboard:dashboard"))


class ExpenseListView(LoginRequiredMixin, ListView):
    template_name = "dashboard/expense/expense_list.html"

    def get_queryset(self):
        user = self.request.user
        return user.participants.all()


class DeleteExpenseView(LoginRequiredMixin, View):
    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        total_transfer_amount = expense.get_totoal_transfer_amount()
        for creditor in expense.get_creditors():
            for debtor in expense.get_debtors():
                insert_data(debtor, creditor, total_transfer_amount)
        expense.delete()
        messages.success(request, "Expense Deleted")
        return HttpResponseRedirect(reverse("dashboard:expense:expense_list"))
