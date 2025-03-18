import random

rows = 5
columns = 6
vector = [[random.randint(1, 6) for _ in range(columns)] for _ in range(rows)]

print("Matriz generada:")
for row in vector:
    print(row)

vector[4] = [0] * columns  

print("\nMatriz después de reemplazar la fila 5 por 0:")
for row in vector:
    print(row)
