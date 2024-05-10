numbers = []

for _ in range(10):
    number = int(input('Ingrese un número entero: '))
    numbers.append(number)

minimum_number = min(numbers)
maximum_number = max(numbers)

print(f'El número más pequeño ingresado es: {minimum_number}')
print(f'El número más grande ingresado es: {maximum_number}')
