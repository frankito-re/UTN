numbers = []

while True:
    exit_or_number = input('Ingrese un numero entero o "exit" para salir: ')
    
    if exit_or_number.lower() == 'exit':
        break
    
    try:
        number = int(exit_or_number)
        numbers.append(number)
    except ValueError:
        print('Por favor, ingrese un número entero válido o "exit" para salir.')

print('Números ingresados:', numbers)
