def dividir_lista(numeros):
    positivos = [num for num in numeros if num >= 0]
    negativos = [num for num in numeros if num < 0]
    
    return positivos, negativos