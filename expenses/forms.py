from django import forms
from django.forms.formsets import BaseFormSet


class AddExpenseFromStep1(forms.Form):
    description = forms.CharField(required=True, widget=forms.Textarea)
    total_cost = forms.DecimalField(required=True, min_value=0.01, max_digits=12, decimal_places=2)
    group = forms.ModelChoiceField(required=True, queryset=None, empty_label="select group")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = self.user.expense_groups.all()


class AddExpenseFromStep2(forms.Form):
    user = forms.EmailField(required=True)
    paid = forms.DecimalField(required=True, min_value=0.00, max_digits=12, decimal_places=2)
    share = forms.DecimalField(required=True, min_value=0.00, max_digits=12, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].widget.attrs["readonly"] = True
