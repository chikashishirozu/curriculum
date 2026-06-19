from math import factorial

e = sum(1 / factorial(n) for n in range(30))

print(f"{e:.20f}")
