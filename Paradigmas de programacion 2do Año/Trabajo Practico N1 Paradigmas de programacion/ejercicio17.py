phrase = str(input('Debes colocar una frase: '))
index_number = int(input('Ingrese la posicion a acceder: '))
symbol = input('Ingrese el simbolo que desea reemplazar: ')

# Las listas son inmutables, entonces debemos convertir la frase en una lista de caracteres
phrase_list = list(phrase)
phrase_list[index_number] = symbol
# Volvemos a unir toda la frase
phrase = ''.join(phrase_list)

print(phrase)
