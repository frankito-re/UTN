number = str(input('Ingrese un number entero: '))

if len(number) < 2:
    if number == '0':
        numero_letras = 'cero'
    elif number == '1':
        numero_letras = 'uno'
    elif number == '2':
        numero_letras = 'dos'
    elif number == '3':
        numero_letras = 'tres'
    elif number == '4':
        numero_letras = 'cuatro'
    elif number == '5':
        numero_letras = 'cinco'
    elif number == '6':
        numero_letras = 'seis'
    elif number == '7':
        numero_letras = 'siete'
    elif number == '8':
        numero_letras = 'ocho'
    elif number == '9':
        numero_letras = 'nueve'
        
    print(f"El número {number} en letras es '{numero_letras}'.")
else:
    print("Error: Debes ingresar un número de un dígito válido.")