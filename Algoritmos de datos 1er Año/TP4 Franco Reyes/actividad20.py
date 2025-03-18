def compare_arrays(array1, array2, find_common):
    # Inicializar conjuntos para los resultados
    common_elements = []
    unique_elements = []
    
    # Buscar elementos comunes
    if find_common:
        for elem in array1:
            if elem in array2 and elem not in common_elements:
                common_elements.append(elem)
        return common_elements
    else:
        # Buscar elementos únicos en array1
        for elem in array1:
            if elem not in array2 and elem not in unique_elements:
                unique_elements.append(elem)
        
        # Buscar elementos únicos en array2
        for elem in array2:
            if elem not in array1 and elem not in unique_elements:
                unique_elements.append(elem)
        
        return unique_elements

array1 = [1, 2, 3, 4, 5]
array2 = [4, 5, 6, 7, 8]

result_common = compare_arrays(array1, array2, True)
print(f"Elementos comunes: {result_common}")

result_unique = compare_arrays(array1, array2, False)
print(f"Elementos no comunes: {result_unique}")