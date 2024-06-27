def invertir(frase):
    if len(frase) <= 1:
        return frase
    return invertir(frase[1:]) + frase[0]

print(invertir('Hola Mundo'))