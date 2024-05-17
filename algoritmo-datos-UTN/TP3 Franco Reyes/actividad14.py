import random

rows = 4
columns = 3
matrix = [[random.randint(1, 100) for _ in range(columns)] for _ in range(rows)]

print('Matriz generada:')
for row in matrix:
    print(row)

# Calcular la suma total de todas las filas
total_sum_rows = sum(sum(row) for row in matrix)
print('\nSuma total de todas las filas:', total_sum_rows)

# Calcular la suma total de todas las columnas
total_sum_columns = sum(sum(matrix[row][col] for row in range(rows)) for col in range(columns))
print('Suma total de todas las columnas:', total_sum_columns)
