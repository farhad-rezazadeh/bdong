from django.contrib import admin

from expenses.models import Expense, Share

# Register your models here.
admin.site.register(Expense)
admin.site.register(Share)
