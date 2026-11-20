import itertools, disposicion as D
from modelo import ASOCIACIONES
pc = D.casos()
ys = {k: D.centro(r)[1] for k, r in pc.items()}
def media(a): return sum(ys[c] for c in ASOCIACIONES[a]) / len(ASOCIACIONES[a])
mejor = None
der = ["CO", "VE", "PD", "AL", "EN"]
izq = ["SA", "PR", "AD", "FI"]
yd_opts = [[ys["CU01"] + i * (ys["CU15"] - ys["CU01"]) / 4 for i in range(5)]]
for od in itertools.permutations(der):
    for yd in yd_opts:
        for yfi in range(300, 2500, 100):
            for (ysa, ypr, yad) in [(300, 900, 1500), (300, 1000, 1700), (330, 800, 1400), (330, 1100, 1900), (500, 1100, 1700)]:
                pa = D.actores(["SA", "PR", "AD", "FI"], od, [ysa, ypr, yad, yfi], yd)
                n = D.cruces(pa, pc)
                if mejor is None or n < mejor[0]:
                    mejor = (n, od, yfi, (ysa, ypr, yad))
print(mejor)
