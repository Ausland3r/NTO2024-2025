n, k = list(map(int, input().split()))
data = sorted(list(map(int, input().split())))

count = data[n - k]
print(count)
# for i in range(k - 1):
#     count = count & data[n-k + i]
#     print(count)
# print(count)


