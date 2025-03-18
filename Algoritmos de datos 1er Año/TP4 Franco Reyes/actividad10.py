def letter_in_word(letter: str):
    words = []
    for _ in range(0, 10):
        word = input('Ingresa una palabra: ')
        words.append(word)
    
    join_words = "".join(words)
    print(f'Cantidad de veces que aparece la letra "{letter}" es: {join_words.count(letter)}')
    
letter_in_word('a')