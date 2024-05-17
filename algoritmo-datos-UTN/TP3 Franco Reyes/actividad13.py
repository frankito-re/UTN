import random

rows = 5
columns = 4

vector = [[random.randint(1, 100) for _ in range(columns)] for _ in range(rows)]

print('\nVector generado:')
for row in vector:
    print(row)

print('\nFilas:')
for row in vector:
    print(row)
    
print('\nColumnas:')
for col in range(columns):
    column = [vector[row][col] for row in range(rows)]
    print(column)
