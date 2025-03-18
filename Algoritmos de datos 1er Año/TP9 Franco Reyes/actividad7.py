def ordenamiento_insercion(nombres):
    
    for i in range(1, len(nombres)):
        key = nombres[i]  
        j = i - 1
        
        while j >= 0 and key < nombres[j]:
            nombres[j + 1] = nombres[j]
            j -= 1
        nombres[j + 1] = key  
    return nombres

# Ejemplo de uso
nombres = ["Carlos", "Ana", "Lucía", "Javier", "Beatriz", "Esteban"]
nombres_ordenados = ordenamiento_insercion(nombres)

# Imprimir la lista ordenada
print("Lista de nombres ordenada:")
for nombre in nombres_ordenados:
    print(nombre)