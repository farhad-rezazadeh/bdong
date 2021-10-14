from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailForm(forms.Form):
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Member Email"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not User.objects.filter(email=email):
            message = "there is no user with this email"
            raise forms.ValidationError(message)
        return email


class GroupNameFrom(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=True,
        label="Group Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter name for group"}),
    )

    def __init__(self, *args, **kwargs):
        self.creator = kwargs.pop("creator", None)
        self.group = kwargs.pop("group", None)
        super(GroupNameFrom, self).__init__(*args, **kwargs)
