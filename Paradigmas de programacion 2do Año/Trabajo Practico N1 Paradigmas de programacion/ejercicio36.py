import numpy as np

# Crear una matriz de 10x10 con valores aleatorios del 1 al 10
matriz = np.random.randint(1, 11, size=(10, 10))

# Sumar todos los valores de la matriz
suma_total = np.sum(matriz)

print("Matriz generada:\n", matriz)
print("\nLa suma total de todos sus elementos es:", suma_total)