# Nombre alumno: Franco Genaro Reyes
class Texto:
    def __init__(self, contenido):
        self.contenido = contenido

    def invertir(self):
        resultado = ''
        for i in range(len(self.contenido) - 1, -1, -1):
            resultado += self.contenido[i]
        return resultado

    def obtener_primera_palabra(self):
        palabra = ''
        for c in self.contenido:
            if c == ' ':
                break
            palabra += c
        return palabra

    def obtener_palabra(self, indice):
        palabra_actual = ''
        contador = 0
        i = 0
        while i < len(self.contenido):
            if self.contenido[i] != ' ':
                palabra_actual += self.contenido[i]
            if self.contenido[i] == ' ' or i == len(self.contenido) - 1:
                if palabra_actual != '':
                    if contador == indice:
                        return palabra_actual
                    contador += 1
                    palabra_actual = ''
            i += 1
        return None  # si no existe la palabra pedida

    def es_palindromo(self):
        limpio = ''
        for c in self.contenido:
            if c != ' ':
                limpio += c.lower()

        invertido = ''
        for i in range(len(limpio) - 1, -1, -1):
            invertido += limpio[i]

        return limpio == invertido

    def contar_letra(self, letra):
        contador = 0
        for c in self.contenido:
            if c == letra:
                contador += 1
        return contador

    def alternar_mayus_minus(self):
        resultado = ''
        usar_mayus = True
        for c in self.contenido:
            if c.isalpha():
                if usar_mayus:
                    resultado += c.upper()
                else:
                    resultado += c.lower()
                usar_mayus = not usar_mayus
            else:
                resultado += c
        return resultado

texto = Texto('Anita lava la tina')

print('Invertido:', texto.invertir())
print('Primera palabra:', texto.obtener_primera_palabra())
print('Palabra 2:', texto.obtener_palabra(2))
print('¿Es palíndromo?:', texto.es_palindromo())
print('Cantidad de "a":', texto.contar_letra('a'))
print('Texto alternado:', texto.alternar_mayus_minus())