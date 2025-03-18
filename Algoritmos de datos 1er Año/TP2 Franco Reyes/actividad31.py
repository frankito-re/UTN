positive_numbers = []
negative_numbers = []

for i in range(10):
    number = int(input(f'Ingrese el numero {i+1}: '))
    
    if number >= 0:
        positive_numbers.append(number)
    else:
        negative_numbers.append(number)
print(f'Los numeros positivos son: {positive_numbers} y los negativos son {negative_numbers}')