def bubble_sort(lista):
    n = len(lista)

    for i in range(n):
        
        for j in range(0, n - i - 1):
            
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

numeros = input("Ingresa una lista de números enteros separados por comas: ")
# Convertir los números ingresados a una lista de enteros
lista_numeros = [int(x) for x in numeros.split(',')]

# Aplico el algoritmo de burbuja
lista_ordenada = bubble_sort(lista_numeros)

# Muestro la lista ordenada
print("Lista ordenada:", lista_ordenada)