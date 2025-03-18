phrase = str(input('Debes colocar una frase: '))
words_counter = 0

for caracter in phrase:
    if caracter == ' ':
        words_counter+=1
        
# Aqui debo sumar la ultima palabra
words_counter+=1
        
print(words_counter)