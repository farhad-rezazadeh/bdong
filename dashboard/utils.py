import redis
from decimal import Decimal, ROUND_UP

r = redis.Redis(host="redis", port=6379, db=0)


def get_balance(user):
    balance = 0
    credit_keys = r.keys(f"{user.pk}:*")
    for credit_key in credit_keys:
        balance += float(r.get(credit_key))
    return balance


def get_total_credit(user):
    credit = 0
    credit_keys = r.keys(f"{user.pk}:*")
    for credit_key in credit_keys:
        if (_ := float(r.get(credit_key))) > 0:
            credit += _
    return credit


def get_total_debt(user):
    debt = 0
    credit_keys = r.keys(f"{user.pk}:*")
    for credit_key in credit_keys:
        if _ := float(r.get(credit_key)) < 0:
            debt += _
    return debt
