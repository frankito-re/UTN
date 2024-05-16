numbers = []
for i in range(5):
    number = int(input(f"Ingrese el número {i + 1}: "))
    numbers.append(number)

print("Números ingresados:")
for number in numbers:
    print(number)