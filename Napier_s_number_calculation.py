from decimal import Decimal, getcontext
from math import factorial

# 計算精度を30桁に設定
getcontext().prec = 30

e = Decimal(0)

n = 0
while True:
    term = Decimal(1) / Decimal(factorial(n))

    # 20桁より十分小さくなったら終了
    if term < Decimal('1e-25'):
        break

    e += term
    n += 1

print(f"e = {e}")
print(f"使用項数 = {n}")
