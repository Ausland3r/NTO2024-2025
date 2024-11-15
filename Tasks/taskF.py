import math


def calculateTau(R, C):
    return R * 10**3 * C * 10 ** -6 * 10**3


R1, C1, R2, C2 = [float(x) for x in input().split()]

tau1 = calculateTau(R1, C1)
tau2 = calculateTau(R2, C2)

uMaxPercent = 0.95
uMinPercent = 0.05

vMax = 5
vMin = 0


tDischargeDC = -tau1 * math.log((vMin - vMax * uMinPercent) / (vMin - vMax*uMaxPercent))
tDischargeDC = max(1, math.ceil(tDischargeDC))

vAfterDischargeDC = vMin - (vMin - vMax*uMaxPercent) * math.exp(-tDischargeDC/tau1)

tChargeDC = -tau1 * math.log((vMax - vMax*uMaxPercent) / (vMax - vAfterDischargeDC))
tChargeDC = max(1, math.ceil(tChargeDC))


tDischargeSTCP = - tau2 * math.log((vMin - vMax * uMinPercent)/ (vMin - vMax*uMaxPercent))
tDischargeSTCP = max(1, math.ceil(tDischargeSTCP))

vAfterDischargeSTCP = vMin - (vMin - vMax*uMaxPercent) * math.exp(-tDischargeSTCP/tau2)

tChargeSTCP = -tau2 * math.log((vMax - vMax*uMaxPercent) / (vMax - vAfterDischargeSTCP))
tChargeSTCP = max(1, math.ceil(tChargeSTCP))



def calculateBit(bitData):
    output = []
    if bitData == '1':
        output.append((0, 1))
        vPulse = vMin - (vMin - vMax*uMaxPercent) * math.exp(-1/tau1)
        tCharge = -tau1 * math.log((vMax - vMax*uMaxPercent) / (vMax - vPulse))
        tCharge = max(1, math.ceil(tCharge))
        output.append((1, tCharge))
    else:
        output.append((0, tDischargeDC))
        output.append((1, tChargeDC))
    return output


n = int(input())
inputArray = input().split(' ')

for value in inputArray:
    byte = int(value, 16)

    for i in range(7, 0, -1):
        bit = (byte >> i) & 1
        for state, time in calculateBit(str(bit)):
            print(f"{state} - {time}")

    print(f"0 - {tDischargeSTCP}")
    print(f"1 - {tChargeSTCP}")



