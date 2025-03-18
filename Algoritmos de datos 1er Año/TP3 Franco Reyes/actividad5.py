import random

random_vector = [random.randint(1, 100) for _ in range(1, 20)]  # Crea un vector con 20 valores aleatorios entre 1 y 100

x_position = int(input('Ingresa la primera posicion del 1 al 20: '))
y_position = int(input(f'Ingresa la segunda posicion del {x_position} al 20: '))

print(f'Los elementos que hay entre las posiciones {x_position} y {y_position} son: {random_vector[x_position : y_position]}')
