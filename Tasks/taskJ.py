import sys

inputString = input()

filterTypes = ['low-pass RC', 'low-pass RL', 'high-pass RC', 'high-pass RL']

if ',' in inputString:
    filterType, typeData = inputString.split(',', 1)
else:
    filterType = inputString
    typeData = ''

filterType = filterType.strip()

if filterType not in filterTypes:
    print('No such type')
    sys.exit()

components = []
if typeData:
    components = typeData.split(',')
    components = [s.strip() for s in components]

if len(components) != 2:
    print('Missing parameters')
    sys.exit()


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


firstComponent = components[0].split(' ')
frequency = components[1].split(' ')

if firstComponent[0] == 'w':
    z = firstComponent
    firstComponent = frequency
    frequency = z


if (len(firstComponent) != 4 or not isfloat(firstComponent[2]) or float(firstComponent[2]) <= 0.0 or
        firstComponent[1] != '=' or (
        firstComponent[0] != 'C' or firstComponent[3] != 'uF') and (
        firstComponent[0] != 'R' or firstComponent[3] != 'Ohm') and (
        firstComponent[0] != 'L' or firstComponent[3] != 'H')):
    print('Wrong format')
    sys.exit()


if len(frequency) != 4 or not isfloat(frequency[2]) or float(frequency[2]) <= 0.0 or frequency[1] != '=' or (
        frequency[0] != 'w' or frequency[3] != 'rad/s'):
    print('Wrong format')
    sys.exit()

if firstComponent[0] == 'C':
    R = 1/(float(frequency[2]) * float(firstComponent[2]) * 10**-6)
    print(f"{filterType}, C = {float(firstComponent[2]):.2f} uF, R = {int(R * 100) / 100.0:.2f} Ohm, w = {float(frequency[2]):.2f} rad/s")

elif firstComponent[0] == 'L':
    R = float(frequency[2]) * float(firstComponent[2])
    print(f"{filterType}, L = {float(firstComponent[2]):.2f} H, R = {int(R * 100) / 100.0:.2f} Ohm, w = {float(frequency[2]):.2f} rad/s")

elif firstComponent[0] == 'R':
    filterType1 = filterType.split(' ')
    if filterType1[1] == 'RC':
        C = (1 / (float(frequency[2]) * float(firstComponent[2]))) / 10**-6
        print(f"{filterType}, C = {int(C * 100) / 100.0:.2f} uF, R = {float(firstComponent[2]):.2f} Ohm, w = {float(frequency[2]):.2f} rad/s")
    elif filterType1[1] == 'RL':
        L = float(frequency[2]) / float(firstComponent[2])
        print(f"{filterType}, L = {int(L * 100) / 100.0:.2f} H, R = {float(firstComponent[2]):.2f} Ohm, w = {float(frequency[2]):.2f} rad/s")

# if (len(argv) != 3):
#     print('Missing parameters')
# else:
#     print(argv)
#     if argv[0] == 'low-pass RC':
# # low-pass RC: w = 1/(RC)
# # low-pass RL: w = R/L
# # high-pass RC: w = 1/(RC)
# # high-pass RL: w = R/L
