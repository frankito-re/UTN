# 3. Lea una palabra e imprima un mensaje indicando si es palíndromo o no. Use pilas. Una palabra
# es palíndromo cuando se lee igual hacia adelante que hacia atr´as. Ejemplo: oso, radar,
# reconocer, rotor, seres, somos, etc.

def invertir_palabra(palabra):
    pila = []
    
    for letra in palabra:
        pila.append(letra)
    
    palabra_invertida = ''
    
    while pila:
        palabra_invertida += pila.pop()
    
    return palabra_invertida

palabra = input("Ingrese una palabra: ")
palabra_invertida = invertir_palabra(palabra)
print(f"Es palíndromo: {palabra_invertida == palabra}")