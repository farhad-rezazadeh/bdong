from django.urls import path, re_path

from expenses.views import CreateExpenseView, SubmitExpense

app_name = "expense"

urlpatterns = [
    path("add/", CreateExpenseView.as_view(), name="add_expense"),
    path("add_expense/", SubmitExpense.as_view(), name="add_expense_submit"),
    re_path(r"^add/step-(?P<step>[1-3])/$", CreateExpenseView.as_view(), name="add_expense_step"),
]
