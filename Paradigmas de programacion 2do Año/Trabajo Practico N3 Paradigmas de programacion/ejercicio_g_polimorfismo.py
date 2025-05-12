# Nombre alumno: Franco Genaro Reyes
class Binario:
    def __init__(self, valor):
        binario_valido = True
        for c in valor:
            if c != '0' and c != '1':
                binario_valido = False
        if binario_valido:
            self.valor = valor
        else:
            self.valor = '0'  # valor por defecto si no es válido

    def a_decimal(self):
        decimal = 0
        potencia = 1
        for digito in self.valor[::-1]:
            if digito == '1':
                decimal += potencia
            potencia *= 2
        return decimal

    def desde_decimal(decimal):
        if decimal == 0:
            return Binario('0')
        binario = ''
        while decimal > 0:
            binario = str(decimal % 2) + binario
            decimal = decimal // 2
        return Binario(binario)

    def sumar(self, otro):
        suma = self.a_decimal() + otro.a_decimal()
        return Binario.desde_decimal(suma)

    def restar(self, otro):
        resta = self.a_decimal() - otro.a_decimal()
        if resta < 0:
            return Binario('0')
        return Binario.desde_decimal(resta)

    def multiplicar(self, otro):
        producto = self.a_decimal() * otro.a_decimal()
        return Binario.desde_decimal(producto)

    def dividir(self, otro):
        if otro.a_decimal() == 0:
            return Binario('0')
        division = self.a_decimal() // otro.a_decimal()
        return Binario.desde_decimal(division)

    def mostrar(self):
        return self.valor

    def es_igual(self, otro):
        return self.a_decimal() == otro.a_decimal()