import numpy as np

f = open('input.txt', 'r')
samples = [float(f.readline()) for _ in range(4000)]

samples = np.array(samples)

fftResult = np.fft.fft(samples)

N = 4000
frequencies = np.fft.fftfreq(N, d=1 / 20000)[:N // 2]

magnitudes = np.abs(fftResult)[:N//2]

indices = np.argsort(-magnitudes)[:4]
maxfrequencies = frequencies[indices]
print(*sorted(np.round(maxfrequencies).astype(int)))
