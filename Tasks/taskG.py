import math

components = [float(x) for x in input().split()]
frequency = int(input())

R1, R2, C1, C2, R3, R4, C3, C4, R5, R6, C5, C6, R7, R8, C7 = components

C1 *= 1e-9
C2 *= 1e-9
C3 *= 1e-9
C4 *= 1e-9
C5 *= 1e-9
C6 *= 1e-9
C7 *= 1e-9

def calculateFSecondOrder(R1, R2, C1, C2):
    return 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))

def calculateFFirstOrder(R, C):
    return 1 / (2 * math.pi * R * C)

f1 = calculateFSecondOrder(R1, R2, C1, C2)
f2 = calculateFSecondOrder(R3, R4, C3, C4)
f3 = calculateFSecondOrder(R5, R6, C5, C6)
f4 = calculateFFirstOrder(R7, C7)

f = (f1 + f2 + f3 + f4) / 4

print(round(f))

mag = 1 / math.sqrt(1 + (frequency / f) ** (2*7))
if mag < 10**-9:
    print(0)
else:
    mag2 = float(f"{mag:.2g}")
    mag2_formated = f"{mag2:.15f}".rstrip('0').rstrip('.')
    print(mag2_formated)
