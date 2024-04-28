phrase = str(input('Ingrese una frase: '))

words_list = []

for letter in phrase:
    if letter != ' ':
        words_list.append(letter)
    
print(words_list)