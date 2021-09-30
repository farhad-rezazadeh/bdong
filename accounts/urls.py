from django.urls import path
from accounts.views import Login, Register, activate

app_name = "accounts"
urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
]
