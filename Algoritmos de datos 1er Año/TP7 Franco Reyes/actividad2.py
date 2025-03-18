# Se almacena una palabra en una pila, de a una letra, y se desea imprimir la palabra invertida.

def invertir_palabra(palabra):
    # Crear la pila como una lista vacía
    pila = []
    
    # Recorrer cada letra de la palabra y agregarla a la pila
    for letra in palabra:
        pila.append(letra)
    
    palabra_invertida = ''
    
    # Desapilar las letras y formar la palabra invertida
    while pila:
        palabra_invertida += pila.pop()
    
    return palabra_invertida

palabra = input("Ingrese una palabra: ")
palabra_invertida = invertir_palabra(palabra)
print(f"Palabra invertida: {palabra_invertida}")
