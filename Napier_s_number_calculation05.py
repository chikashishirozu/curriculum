from decimal import Decimal, getcontext

DIGITS = 10000

# 誤差対策で余分に50桁
getcontext().prec = DIGITS + 50

e = Decimal(1)
term = Decimal(1)

n = 1

while term > Decimal(10) ** (-(DIGITS + 20)):
    term /= n
    e += term
    n += 1

print(str(+e)[:DIGITS + 2])
