import random

random_vector = [random.randint(1, 100) for _ in range(0, 30)]

x_position = int(input('Ingresa la primera posicion del 0 al 30: '))
y_position = int(input(f'Ingresa la segunda posicion del {x_position} al 30: '))

print(f'Los elementos que hay entre las posiciones (sin intercambiar) {x_position} y {y_position} son: {random_vector[x_position -1 : y_position]}')

random_vector[x_position -1], random_vector[y_position -1] = random_vector[y_position -1], random_vector[x_position -1]

print(f'Los elementos que hay entre las posiciones (intercambiadas) {x_position} y {y_position} son: {random_vector[x_position -1 : y_position]}')

