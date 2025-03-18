import random

random_vector = [random.randint(1, 50) for _ in range(0, 18)]
average_vector = sum(random_vector) / len(random_vector)

print(int(average_vector))