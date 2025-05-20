import numpy as np
from scipy.optimize import brentq


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


def tf1(s):
    numerator = 1
    denominator = C1 * C2 * R1 * R2 * s ** 2 + C2 * (R1 + R2) * s + 1
    return numerator / denominator


def tf2(s):
    numerator = 1
    denominator = C3 * C4 * R3 * R4 * s ** 2 + C4 * (R3 + R4) * s + 1
    return numerator / denominator


def tf3(s):
    numerator = 1
    denominator = C5 * C6 * R5 * R6 * s ** 2 + C6 * (R5 + R6) * s + 1
    return numerator / denominator


def tf4(s):
    numerator = R8 / R7
    denominator = R8 * C7 * s + 1
    return numerator / denominator


def Htotal(s):
    return tf1(s) * tf2(s) * tf3(s) * tf4(s)

def magnitudeDb(freqHz):
    omega = 2 * np.pi * freqHz
    s = 1j * omega
    H = Htotal(s)
    mag = np.abs(H)
    magDb = 20 * np.log10(mag)
    return magDb

def findFrequenciesForMagnitude(targetMagnitude = -3):
    magL = magnitudeDb(0)

    freqR = 1
    while True:
        magR = magnitudeDb(freqR)
        if (magL - targetMagnitude)*(magR-targetMagnitude)<0.0:
            return brentq(lambda f: magnitudeDb(f) - targetMagnitude,
                          freqR-1, freqR, xtol=1e-12, rtol=1e-8, maxiter=1000)
        freqR+=1
        magL=magR


freq_n = findFrequenciesForMagnitude()
if freq_n < 100.0:
    freq = round(freq_n)
elif freq_n >= 100.0 and freq_n <= 1000.0:
    freq = int(round(freq_n / 10.0) * 10)
elif freq_n > 1000.0:
    freq = int(round(freq_n / 100.0) * 100)

print(freq)
mag = (1/np.sqrt(1+(frequency/freq_n)**(2*7)))
if mag < 10**-9:
    print(0)
else:
    mag2 = float(f"{mag:.2g}")
    mag2_formated = f"{mag2:.15f}".rstrip('0').rstrip('.')
    print(mag2_formated)

