# Con lista
phrase = str(input('Ingrese una frase: '))

phrase_word_list = phrase.split()

print(f'Palabras en lista: {phrase_word_list}, su cantidad: {len(phrase_word_list)}')

# Sin lista
phrase_two = input("Ingrese una frase: ")

phrase_len = 0

word = False
for caracter in phrase_two :
    if caracter.isalnum():
        word = True
    elif word:
        phrase_len += 1
        word = False

if word:
    phrase_len += 1

print(f"La frase tiene {phrase_len} palabra(s).")