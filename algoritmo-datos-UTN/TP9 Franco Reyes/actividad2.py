def selection_sort(arr):
    
    for i in range(len(arr)):
        
        min_idx = i
        
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
    
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr

# Lista de números
numeros = [6, 2, 4, 8, 3, 7, 5]

# Ordeno la lista
numeros_ordenados = selection_sort(numeros)

# Muestro la lista ordenada
print("Números ordenados:", numeros_ordenados)