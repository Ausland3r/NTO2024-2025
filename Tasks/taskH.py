data = [[int(x) for x in input().split()] for _ in range(16)]

data.sort(key=lambda x: (x[0], x[1], x[2], x[3]))


data2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
data2[0][0] = data[0][4]
data2[1][0] = data[2][4]
data2[2][0] = data[1][4]
data2[3][0] = data[3][4]

# print(data2)
data2[0][2] = data[4][4]
data2[1][2] = data[6][4]
data2[2][2] = data[5][4]
data2[3][2] = data[7][4]
# print(data2)

data2[0][1] = data[8][4]
data2[1][1] = data[10][4]
data2[2][1] = data[9][4]
data2[3][1] = data[11][4]
# print(data2)

data2[0][3] = data[12][4]
data2[1][3] = data[14][4]
data2[2][3] = data[13][4]
data2[3][3] = data[15][4]
# print(data2)

dataOut = ["A'B'C'D'", "AB'C'D'", "A'BC'D'", "ABC'D'", "A'B'CD'", "AB'CD'", "A'BCD'", "ABCD'", "A'B'C'D", "AB'C'D", "A'BC'D", "ABC'D", "A'B'CD", "AB'CD", "A'BCD", "ABCD"]

# print(data)
# for i in range(4):
#     print(data2[i])

dataOut2 = []
# print(*dataOut, sep=" OR ")
pos = 0
for i in range(4):
    for j in range(4):
        # print(dataOut[pos])
        if data2[i][j] == 1:
            # print(dataOut[pos], i, j)
            dataOut2.append(dataOut[pos])
        pos += 1

print("Карта Карно:")
for i in range(4):
    print(data2[i])

print("Минимизированное логическое выражение:", end=" ")
print(*dataOut2, sep=" OR ")

# for i in range(16):
    # print(data[i])
