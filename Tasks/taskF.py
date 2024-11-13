import math


def calculateTau(R, C):
    return R * 10**3 * C * 10 ** -6 * 10**3


R1, C1, R2, C2 = [float(x) for x in input().split()]

tau1 = calculateTau(R1, C1)
tau2 = calculateTau(R2, C2)


uMaxPercent = 0.95
uMinPercent = 0.05

tDischargeDc = max(1, math.ceil(tau1 * math.log(uMaxPercent / uMinPercent)))
tChargeDc = max(1, math.ceil(tau1 * math.log((1 - uMinPercent) / (1 - uMaxPercent))))

tDischargeDStcp = max(1, math.ceil(tau2 * math.log(uMaxPercent / uMinPercent)))
tChargeStcp = max(1, math.ceil(tau2 * math.log((1 - uMinPercent) / (1 - uMaxPercent))))


def calculateBit(bitData):
    output = []
    if bitData == '1':
        output.append((0, 1))
        vPulse = uMaxPercent * math.exp(-1/tau1)
        output.append((1, max(1, math.ceil(tau1 * math.log((1 - vPulse) / (1 - uMaxPercent))))))
    else:
        output.append((0, tDischargeDc))
        output.append((1, tChargeDc))
    return output


n = int(input())
inputArray = input().split(' ')

for value in inputArray:
    byte = int(value, 16)

    for state, time in calculateBit('1'):
        print(f"{state} - {time}")

    for i in range(6, 0, -1):
        bit = (byte >> i) & 1
        for state, time in calculateBit(str(bit)):
            print(f"{state} - {time}")

    print(f"0 - {tDischargeDStcp}")
    print(f"1 - {tChargeStcp}")


