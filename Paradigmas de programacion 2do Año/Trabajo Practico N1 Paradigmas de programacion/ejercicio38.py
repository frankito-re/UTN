import numpy as np

# Vector con los valores que quieres en la diagonal principal
valores_diagonal = [1, 2, 3, 4, 5, 6]

# Crear una matriz diagonal con estos valores
matrix = np.diag(valores_diagonal)

file_url = '<path>/matriz.txt'

with open(file_url, 'w') as file:
    for vector in matrix:
        vector_list = [str(num) for num in vector]
        print(vector_list)
        line = ' '.join(vector_list)
        file.write(line + '\n')