pair_numbers = []
odd_numbers = []

while True:
    number = int(input('Ingrese un numero entero o ingresa el numero "99" para salir: '))
    if number == 99:
        break
    
    if number % 2 != 0:
        odd_numbers.append(number)
        
    pair_numbers.append(number)
    
print(f'La suma de los numeros pares es: {sum(pair_numbers)}')

if len(odd_numbers) != 0:
    print(f'Los numeros impares son: {odd_numbers}')