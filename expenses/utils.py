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
