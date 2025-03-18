def caracter_index(character: str, string: str):
    try:
        index = string.index(character)
        return index
    except ValueError:
        return -1
    
print(caracter_index('a', 'hola'))