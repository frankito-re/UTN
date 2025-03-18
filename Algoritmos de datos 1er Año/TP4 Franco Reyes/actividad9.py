def letter_in_word(word: str, letter: str):
    # Puro codigo perrin 😎
    letter_count = 0
    for l in word:
        if l == letter:
            letter_count+=1
    print(letter_count)
    
    # Tambien se puede hacer con count()
    letter_count = word.count(letter)
    print(letter_count)
    
letter_in_word('hola', 'a')