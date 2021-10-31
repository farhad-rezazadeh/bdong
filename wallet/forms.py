from django import forms


class WithdrawFrom(forms.Form):
    amount = forms.DecimalField(required=True, min_value=0.01, max_digits=12, decimal_places=2)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount > self.user.wallet:
            message = "Asked amount is higher than deposit"
            raise forms.ValidationError(message)
        return amount

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(WithdrawFrom, self).__init__(*args, **kwargs)


class ChargeFrom(forms.Form):
    amount = forms.DecimalField(required=True, min_value=0.01, max_digits=12, decimal_places=2)
