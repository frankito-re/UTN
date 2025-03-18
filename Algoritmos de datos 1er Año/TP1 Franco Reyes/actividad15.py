first_word = str(input('Ingresar palabra: '))
second_word = str(input('Ingresar palabra: '))

len_first_word = len(first_word)
len_second_word = len(second_word)

if (len_first_word == len_second_word):
    print(f'Misma logitud: {len_first_word}')
else:
    print(f'Longitud mayor: {max(len_first_word, len_second_word)}')
    print(f'Longitud menor: {min(len_first_word, len_second_word)}')