# Nombre alumno: Franco Genaro Reyes
class Binario:
    def __init__(self, binario_str):
        # Validamos que solo tenga 0s y 1s
        valido = True
        for c in binario_str:
            if c != '0' and c != '1':
                valido = False
        if valido:
            self.valor = binario_str
        else:
            self.valor = '0'

    def a_decimal(self):
        decimal = 0
        potencia = 1
        for c in self.valor[::-1]:
            if c == '1':
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

    def mostrar(self):
        return self.valor