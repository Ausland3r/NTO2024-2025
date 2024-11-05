n = int(input())
sec =  list(map(int, input().split()))

a = 1/3
b = 1/2
c = 1/6
p = c/a-b**2/(3*a**2)

count = 0
for i in range(n):
    q = 2 * b**3 / (27 * a**3) - b * c / (3 * a**2) - sec[i] / a
    Q1 = (p / 3)**3 + (q / 2)**2
    alpha = (-q / 2 + Q1**0.5)**(1 / 3)
    beta = (-q / 2 - Q1**0.5)**(1 / 3)
    y = alpha + beta
    x = y - b / (3 * a)
    x = round(x, 9)
    count+=int(x)
print(count)