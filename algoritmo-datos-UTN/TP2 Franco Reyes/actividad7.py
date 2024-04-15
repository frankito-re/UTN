word = str(input('Ingrese una palabra: '))

for letter in range(len(word)):
    if letter % 2 == 1:
        print(word[letter])