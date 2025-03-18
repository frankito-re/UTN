word = str(input('Ingrese una frase: '))
letter_selected = str(input('Ingrese una letra: '))

counter = word.count(letter_selected)

print(f"La letra '{letter_selected}' aparece {counter} veces en la frase.")

