# Implementar una funcion que invierta el orden de las palabras de una frase. Ejemplo: Si
# recibe la frase Buen día! retornara día! Buen
def invert_words(phrase:str):
    words = phrase.split()
    inverted_phrase = []
    while words:
        word = words.pop()
        inverted_phrase.append(word)
    return ' '.join(inverted_phrase)

print(invert_words('Buen dia!'))