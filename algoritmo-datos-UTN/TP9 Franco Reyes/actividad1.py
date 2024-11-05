def insertion_sort(arr):
    
    for i in range(1, len(arr)):
        key = arr[i]

        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key  
    return arr

# Lista de numeros
numeros = [76, 21, 34, 68, 31, 27, 53]

# Ordeno la lista
numeros_ordenados = insertion_sort(numeros)

# Aca voy a mostrar la lista ordenada 
print("Numeros ordenados:", numeros_ordenados)