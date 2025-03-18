import random
# Paso 1: Generar una lista de 10 números enteros aleatorios entre 1 y 100
lista_numeros = [random.randint(1, 100) for _ in range(10)]
print("Lista generada:", lista_numeros)
# Paso 2: Pedir al usuario un número
numero_usuario = int(input("Introduce un número a buscar: "))
# Paso 3: Búsqueda secuencial
encontrado = False
for indice, numero in enumerate(lista_numeros):
    if numero == numero_usuario:
        encontrado = True
        print(f"El número {numero_usuario} se encuentra en la posición {indice}.")
        break
# Si no se encuentra el número
if not encontrado:
    print(f"El número {numero_usuario} no está en la lista.")