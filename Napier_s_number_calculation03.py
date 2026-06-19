from decimal import Decimal, getcontext

getcontext().prec = 40

e = Decimal(1)
term = Decimal(1)
n = 1

while term > Decimal('1e-30'):
    term /= n
    e += term
    n += 1

print(e)
