import random

rows = 4
columns = 3

vector = [[random.randint(1, 100) for _ in range(columns)] for _ in range(rows)]

print('Vector generado:')
for rows in vector:
    print(rows)