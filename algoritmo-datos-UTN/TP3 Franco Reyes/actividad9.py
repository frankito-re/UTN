import random

random_vector = [random.randint(1, 50) for _ in range(0, 18)]

max_number = max(random_vector)
min_number = min(random_vector)

print(f'El valor maximo es: {max_number} y el minimo es: {min_number}')