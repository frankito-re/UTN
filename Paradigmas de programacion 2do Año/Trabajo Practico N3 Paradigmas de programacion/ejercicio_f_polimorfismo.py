# Nombre alumno: Franco Genaro Reyes
class Complejo:
    def __init__(self, real, imaginario):
        self.real = real
        self.imaginario = imaginario

    def __add__(self, otro):
        return Complejo(self.real + otro.real, self.imaginario + otro.imaginario)

    def __sub__(self, otro):
        return Complejo(self.real - otro.real, self.imaginario - otro.imaginario)

    def __mul__(self, otro):
        real = self.real * otro.real - self.imaginario * otro.imaginario
        imag = self.real * otro.imaginario + self.imaginario * otro.real
        return Complejo(real, imag)

    def __eq__(self, otro):
        return self.real == otro.real and self.imaginario == otro.imaginario

    def __str__(self):
        signo = '+' if self.imaginario >= 0 else '-'
        return f'{self.real} {signo} {abs(self.imaginario)}i'

c1 = Complejo(2, 3)
c2 = Complejo(1, -4)

print('Suma:', c1 + c2)
print('Resta:', c1 - c2)
print('Multiplicación:', c1 * c2)
print('¿Son iguales?', c1 == c2)