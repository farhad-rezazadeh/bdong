import redis
from decimal import Decimal, ROUND_UP

r = redis.Redis(host="redis", port=6379, db=0)


def insert_data(creditor, debtor, total_transfer_amount):
    transfer_amount = (
        (debtor["share"] - debtor["paid"]) * (creditor["paid"] - creditor["share"])
    ) / total_transfer_amount
    transfer_amount = float(Decimal(transfer_amount).quantize(Decimal(".00"), rounding=ROUND_UP))
    r.incrbyfloat(f"{creditor['user']}:{debtor['user']}", transfer_amount)
    r.incrbyfloat(f"{debtor['user']}:{creditor['user']}", -transfer_amount)


def get_credits(creditor):
    credit_list = list()
    credit_keys = r.keys(f"{creditor.pk}:*")
    for credit_key in credit_keys:
        _ = float(r.get(credit_key))
        if _ > 0:
            credit_list.append((credit_key.decode("ascii").split(":")[1], _))
    return credit_list


def get_debts(debtor):
    debt_list = list()
    debt_keys = r.keys(f"*:{debtor.pk}")
    for debt_key in debt_keys:
        _ = float(r.get(debt_key))
        if _ > 0:
            debt_list.append((debt_key.decode("ascii").split(":")[0], _))
    return debt_list


def get_balance(debtor, creditor):
    return float(r.get(f"{creditor}:{debtor}").decode("ascii"))


def settle_up(debtor, creditor):
    r.set(f"{debtor}:{creditor}", float(0))
    r.set(f"{creditor}:{debtor}", float(0))
