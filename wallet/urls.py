from django.urls import path

from wallet.views import WalletView, WithdrawWalletView, ChargeWalletView

app_name = "wallet"

urlpatterns = [
    path("", WalletView.as_view(), name="wallet"),
    path("withdraw/", WithdrawWalletView.as_view(), name="withdraw_wallet"),
    path("charge/", ChargeWalletView.as_view(), name="charge_wallet"),
]
