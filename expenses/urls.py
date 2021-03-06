from django.urls import path, re_path

from expenses.views import (
    CreateExpenseView,
    SubmitExpense,
    ExpenseListView,
    DeleteExpenseView,
    AccountancyView,
    SettleUpView,
)

app_name = "expense"

urlpatterns = [
    path("add/", CreateExpenseView.as_view(), name="add_expense"),
    path("add_expense/", SubmitExpense.as_view(), name="add_expense_submit"),
    re_path(r"^add/step-(?P<step>[1-3])/$", CreateExpenseView.as_view(), name="add_expense_step"),
    path("expense_list/", ExpenseListView.as_view(), name="expense_list"),
    path("delete_expense/<int:pk>/", DeleteExpenseView.as_view(), name="delete_expense"),
    path("accountancy/", AccountancyView.as_view(), name="accountancy"),
    path("settle_up/<int:pk>/", SettleUpView.as_view(), name="settle_up"),
]
