import random

throws = [random.randint(1, 6) for _ in range(2500)]

throws_sum = sum(throws)

print(f'La suma de todos los valores es: {throws_sum} y su promedio es {throws_sum / 2500}')