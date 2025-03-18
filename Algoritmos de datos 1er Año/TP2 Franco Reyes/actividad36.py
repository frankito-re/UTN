import random

a = int(input('Ingrese el primer número positivo (a): '))
b = int(input('Ingrese el segundo número positivo mayor que el primero (b): '))

if a >= b:
    print('Error: b debe ser mayor que a.')
else:
    print(f'Números en el intervalo [{a}, {b}]:', list(range(a, b+1)))

    selected_number = random.randint(a, b)

    lives = 10
    success = False

    while lives > 0:
        guess = int(input(f'Intento {11 - lives}: Adivina el número seleccionado: '))

        if guess == selected_number:
            success = True
            break
        else:
            lives -= 1
            print('Pucha, ese no era el número. Intenta de nuevo.')

    if success:
        print(f'¡Felicidades! Has adivinado el número {selected_number}.')
    else:
        print(f'Has agotado tus vidas. El número seleccionado era {selected_number}. Mejor suerte la próxima vez.')
