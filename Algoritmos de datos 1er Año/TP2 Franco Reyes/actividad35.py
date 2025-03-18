number = input('Ingrese un número de 6 cifras: ')

if len(number) != 6:
    print('Error: Por favor, ingrese un número de 6 cifras exactamente.')
else:
    inverted_number = number[::-1]
    print(f'El número ingresado es {number}, invertido es: {inverted_number}')
