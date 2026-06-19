from decimal import Decimal, getcontext
from math import factorial

DIGITS = 1000

# 余裕を持たせる
getcontext().prec = DIGITS + 20

C = 426880 * Decimal(10005).sqrt()

S = Decimal(0)

# 1000桁なら72項程度で十分
for k in range(72):

    numerator = (
        Decimal(factorial(6 * k))
        * (13591409 + 545140134 * k)
    )

    denominator = (
        Decimal(factorial(3 * k))
        * (Decimal(factorial(k)) ** 3)
        * (Decimal(640320) ** (3 * k))
    )

    term = numerator / denominator

    if k % 2:
        S -= term
    else:
        S += term

pi = C / S

print(str(+pi)[:DIGITS + 2])
