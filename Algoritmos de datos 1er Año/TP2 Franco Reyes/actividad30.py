# que crack que soy programando
import time

countdown_number = int(input('Ingresar numero para la cuenta regresiva: '))
selected_loop = int(input('Ingresa el loop de preferencia, 1 es "for" y 2 es "while": '))

if countdown_number <= 0:
    print('El numero ingresado es negativo')
else:
    countdown_number_two = 0
    if selected_loop == 1:
        for number in range(1, countdown_number+1):
            time.sleep(1)
            print(number)
    elif selected_loop == 2:
        while countdown_number_two < countdown_number:
            time.sleep(1)
            countdown_number_two += 1
            print(countdown_number_two)
    else:
        print('Opción de bucle no válida')
