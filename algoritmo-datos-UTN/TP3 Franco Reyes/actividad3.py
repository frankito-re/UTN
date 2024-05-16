import random

selected_number = int(input('Ingrese un numero para comprobar si se encuentra dentro del vector:'))

vector = [random.randint(5, 30) for _ in range(20)]

if selected_number in vector:
    print(f"El número {selected_number} está en el vector.")
else:
    print(f"El número {selected_number} no está en el vector.")