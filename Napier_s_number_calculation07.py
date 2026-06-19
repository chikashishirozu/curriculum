from math import factorial

DIGITS = 10000

N = 3500

f = factorial(N)

s = 0

for k in range(N + 1):
    s += f // factorial(k)

scale = 10 ** DIGITS

e_digits = (s * scale) // f

e_str = str(e_digits)

print(e_str[0] + "." + e_str[1:])
