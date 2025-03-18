# Dada una frase ingresada por el usuario, determinar cuantas palabras de longitud par
# contiene. (La frase “hola Frodo, y Bilbo?” contiene 1 sola palabra de longitud par)
phrase = str(input('Debes colocar una frase: '))
phrase_words_list = phrase.split()
pair_words_counter = 0

for i in phrase_words_list:
    if len(i) % 2 == 0:
        pair_words_counter+=1
        
print(pair_words_counter)