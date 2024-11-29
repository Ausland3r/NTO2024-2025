import math

number = float(input("Enter a number: "))

if number < 10**-9:
    print(0)
else:
    number2 = float(f"{number:.2g}")
    # number = 1e-6
    formatted_number = f"{number2:.15f}".rstrip('0').rstrip('.')
    print(f"Число: {formatted_number}")
    print(number2)