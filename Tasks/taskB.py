n, k = list(map(int, input().split()))
a = list(map(int, input().split()))

result = 0
for bit in range(29, -1, -1):
    numbers_with_bit = []
    for num in a:
        if (num & (1 << bit)) and (num & result) == result:
            numbers_with_bit.append(num)



