import time
start = time.time()

import math

import numpy as np
# import matplotlib.pyplot as plt
from scipy.optimize import brentq

# Заданные значения компонентов
R1 = 237000  # Ом
R2 = 237000  # Ом
C1 = 15e-9  # Фарад
C2 = 12e-9  # Фарад
R3 = 158000  # Ом
R4 = 158000  # Ом
C3 = 32e-9  # Фарад
C4 = 12e-9  # Фарад
R5 = 154000  # Ом
R6 = 154000  # Ом
C5 = 94e-9  # Фарад
C6 = 4.7e-9  # Фарад
R7 = 316000  # Ом
R8 = 316000  # Ом
C7 = 10e-9  # Фарад


# Функции для расчета передаточных функций каждого каскада
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


# Общая передаточная функция
def H_total(s):
    return tf1(s) * tf2(s) * tf3(s) * tf4(s)


# Функция для расчета модуля передаточной функции в дБ при заданной частоте
def magnitude_db(freq_hz):
    omega = 2 * np.pi * freq_hz
    s = 1j * omega
    H = H_total(s)
    mag = np.abs(H)
    mag_db = 20 * np.log10(mag)
    return mag_db


# Функция для нахождения частоты по заданной амплитуде в дБ с использованием brentq
def find_frequencies_for_magnitude(desired_magnitude_db, freq_min=1, freq_max=100000, num_points=10000):
    freqs = np.logspace(np.log10(freq_min), np.log10(freq_max), num_points)
    print(freqs)
    mags_db = magnitude_db(freqs)

    # Найдем все частоты, где ЛАЧХ пересекает заданную амплитуду
    crossings = []
    for i in range(len(freqs) - 1):
        # Проверяем, что между соседними точками происходит пересечение уровня амплитуды
        if (mags_db[i] - desired_magnitude_db) * (mags_db[i + 1] - desired_magnitude_db) < 0:
            # Есть пересечение между freqs[i] и freqs[i+1]
            try:
                freq_root = brentq(
                    lambda f: magnitude_db(f) - desired_magnitude_db,
                    freqs[i],
                    freqs[i + 1],
                    xtol=1e-12,
                    rtol=1e-8,
                    maxiter=1000
                )
                crossings.append(freq_root)
            except ValueError:
                # Не удалось найти корень в этом интервале
                pass

    # Удаляем близкие друг к другу решения (в пределах 1 Гц), чтобы избежать дублирования
    unique_crossings = []
    print(crossings)
    for freq in crossings:
        if not any(np.isclose(freq, existing_freq, atol=1e-2) for existing_freq in unique_crossings):
            unique_crossings.append(freq)

    return unique_crossings


# Пример использования
desired_magnitude_db = -3  # Заданная амплитуда в дБ
crossing_frequencies = find_frequencies_for_magnitude(desired_magnitude_db)

if crossing_frequencies:
    print(f"Частоты при амплитуде {desired_magnitude_db} дБ:")
    for idx, freq in enumerate(crossing_frequencies, 1):
        print(f"{idx}. {freq:.2f} Гц", idx, freq, freq*2*math.pi)
else:
    print("Не найдено частоты, соответствующей заданной амплитуде.")

# Построение ЛАЧХ
# freqs_plot = np.logspace(1, 5, 1000)  # Частоты от 10^1 до 10^5 Гц
# mags_db_plot = magnitude_db(freqs_plot)

# plt.figure(figsize=(10, 6))
# plt.semilogx(freqs_plot, mags_db_plot, label='ЛАЧХ')
# plt.xlabel('Частота (Гц)')
# plt.ylabel('Амплитуда (дБ)')
# plt.title('Логарифмическая амплитудно-частотная характеристика (ЛАЧХ)')
# plt.grid(which='both', linestyle='--', linewidth=0.5)
# plt.axhline(y=desired_magnitude_db, color='r', linestyle='--', label=f'{desired_magnitude_db} дБ')
#
# for freq in crossing_frequencies:
#     plt.axvline(x=freq, color='r', linestyle='--')
#
# plt.legend()
# plt.tight_layout()
# plt.show()
print(freq)
print(1/math.sqrt(1+(35.0/round(freq))**(2*7)))

print(time.time()-start)

print(magnitude_db(0), magnitude_db(1), magnitude_db(2))
