# Generar la siguiente matriz e imprimirla en pantalla, utilizando Numpy.
# Ademas se debera almacenar en un archivo de texto llamado matriz.txt sin utilizar metodos de Numpy,
# es decir sin utilizar comandos como savetofile y del estilo, 
# debera resolverlo artesanalmente, solo con lo esencial, condicionales, bucles, variables:
# 1 0 0 0 0 0
# 0 2 0 0 0 0
# 0 0 3 0 0 0
# 0 0 0 4 0 0
# 0 0 0 0 5 0
# 0 0 0 0 0 6
import numpy as np

# Vector con los valores que quieres en la diagonal principal
valores_diagonal = [1, 2, 3, 4, 5, 6]

# Crear una matriz diagonal con estos valores
matrix = np.diag(valores_diagonal)

file_url = '/Users/d3ksur/Proyectos Mios/UTN/Paradigmas de programacion 2do Año/Trabajo Practico N1 Paradigmas de programacion/matriz.txt'

with open(file_url, 'w') as file:
    for vector in matrix:
        vector_list = [str(num) for num in vector]
        print(vector_list)# convierte números a strings
        line = ' '.join(vector_list)                # los une con espacios
        file.write(line + '\n')                     # lo escribe en el archivo