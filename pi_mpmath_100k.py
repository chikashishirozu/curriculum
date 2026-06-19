from mpmath import mp
mp.dps = 100000
pi = mp.pi
with open("pi_mpmath.txt", "w") as f:
    f.write(str(pi))
