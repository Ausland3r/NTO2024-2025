import bisect
import sys


try:
    with open("input.txt", "r") as f:
        n = int(f.readline().strip())
        times = list(map(int, f.readline().strip().split()))
except FileNotFoundError:
    n = int(input().strip())
    times = list(map(int, input().strip().split()))

cumulative_durations = []
current_duration = 0
k = 1

while current_duration <= 10**9:
    current_duration += k * k
    cumulative_durations.append(current_duration)
    k += 1

total_ads = 0
for time in times:
    ads_watched = bisect.bisect_right(cumulative_durations, time)
    total_ads += ads_watched

try:
    with open("output.txt", "w") as f:
        f.write(str(total_ads))
except FileNotFoundError:
    print(total_ads)