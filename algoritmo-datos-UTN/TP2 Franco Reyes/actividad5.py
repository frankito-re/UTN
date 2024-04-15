first_word = input('Ingrese la primera palabra: ')
second_word = input('Ingrese la segunda palabra: ')

# Mostrar las palabras concatenadas de diferentes formas
print("Concatenación 1:", first_word + second_word)  # Concatenación directa usando el operador +
print("Concatenación 2:", first_word, second_word)  # Concatenación con espacio usando la coma en print()
print("Concatenación 3:", first_word, end="")  # Concatenación sin espacio usando end=""
print(second_word)  # Mostrar la segunda palabra en la misma línea

# Mostrar la diferencia entre concatenación y mostrar una seguida de otra
concatenacion = first_word + second_word
print("Concatenación final:", concatenacion)  # Mostrar la concatenación completa
print("Mostrar una seguida de otra:", first_word, second_word)  # Mostrar las palabras una después de la otra
