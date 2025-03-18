import random

lista = [random.randint(1, 6) for _ in range(10)]

for i in range(len(lista)):
    if lista[i] == 1:  # Acceder y modificar directamente la lista
        lista[i] = 0
        
print(lista)