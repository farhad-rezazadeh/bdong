from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from wallet.forms import ChargeFrom, WithdrawFrom


class WalletView(LoginRequiredMixin, View):
    def get(self, request):
        charge_form = ChargeFrom()
        withdraw_form = WithdrawFrom(user=request.user)
        context = {"charge_form": charge_form, "withdraw_form": withdraw_form}
        return render(request, "dashboard/wallet/wallet.html", context=context)


class WithdrawWalletView(LoginRequiredMixin, View):
    def post(self, request):
        form = WithdrawFrom(request.POST, user=request.user)
        success = False
        if form.is_valid():
            request.user.wallet -= form.cleaned_data["amount"]
            request.user.save()
            messages.success(request, "selected amounted transfer to your credit card")
            form = WithdrawFrom(user=request.user)
            success = True
        context = {"withdraw_form": form, "success": success}
        return render(request, "dashboard/wallet/withdraw_form.html", context=context)


class ChargeWalletView(LoginRequiredMixin, View):
    def post(self, request):
        form = ChargeFrom(request.POST)
        success = False
        if form.is_valid():
            request.user.wallet += form.cleaned_data["amount"]
            request.user.save()
            messages.success(request, "wallet charged")
            form = ChargeFrom()
            success = True
        context = {"charge_form": form, "success": success}
        return render(request, "dashboard/wallet/charge_form.html", context=context)
