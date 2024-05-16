numbers = []
for i in range(5):
    number = int(input(f"Ingrese el número {i + 1}: "))
    numbers.append(number)

print("Números ingresados en orden inverso:")
for i in range(len(numbers) - 1, -1, -1):
    print(numbers[i])