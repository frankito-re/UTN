# Ordene los siguientes numeros 76, 21, 34, 68, 31, 27, 53 utilizando el algoritmo de
# ordenacion por Insercion (Insertion Sort)

def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]

# Ejemplo
lista = [3, 2, 1]
bubble_sort(lista)
print("Lista ordenada:", lista)
