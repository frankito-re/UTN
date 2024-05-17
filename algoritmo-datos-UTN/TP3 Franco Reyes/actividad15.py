import random

rows = 4
columns = 3

total_rows_sum = []
total_columns_sum = []

vector = [[random.randint(1, 100) for _ in range(columns)] for _ in range(rows)]

print("\nVector generado:")
for row in vector:
    print(row)

# Suma de las filas
for row in vector:
    total_rows_sum.append(sum(row))
    
print(f'\nLa suma de las filas es: {total_rows_sum}')

# Suma de las columnas
for col in range(columns):
    column = [vector[row][col] for row in range(rows)]
    total_columns_sum.append(sum(column))

print(f'\nLa suma de las columnas es: {total_columns_sum}')