input_phrase = str(input('Debes colocar una frase: '))

# Primera manera: Usando ciclo for
def inverted_phrase1(phrase):
    inverted_phrase = ''  # String vacío para ir acumulando caracteres invertidos
    for i in range(len(phrase) - 1, -1, -1):
        inverted_phrase += phrase[i]
    return inverted_phrase

print(inverted_phrase1(input_phrase))

# Segunda manera: Usando slicing
def inverted_phrase2(phrase):
    return phrase[::-1]
        
print(inverted_phrase2(input_phrase))

# Tercera manera: Usando listas y la función join()
def inverted_phrase3(phrase):
    characters_list = list(phrase)
    inverted_phrase = "".join([characters_list[i] for i in range(len(characters_list)-1, -1, -1)])
    return inverted_phrase

inverted_phrase3(input_phrase)