import random

# Generar un archivo con 50 números aleatorios
with open('nros.txt', 'w') as file:
    for _ in range(50):
        file.write(f"{random.randint(1, 100)}\n")

# Leer los números del archivo
with open('nros.txt', 'r') as file:
    numeros = [int(line.strip()) for line in file]

# Ordenar los números
numeros_ordenados = sorted(numeros)

# Guardar los números ordenados en un nuevo archivo
with open('ordenado.txt', 'w') as file:
    for numero in numeros_ordenados:
        file.write(f"{numero}\n")

print("Archivo 'ordenado.txt' generado correctamente.")