# Nombre alumno: Franco Genaro Reyes
class Temperatura:
    def __init__(self, valor, unidad='C'):
        self.valor = valor
        self.unidad = unidad.upper()
    
    def conversion_unidad(self, destino):
        destino = destino.upper()
        if self.unidad == 'C':
            if destino == 'F':
                return (self.valor * 9/5) + 32
            elif destino == 'K':
                return self.valor + 273.15
            elif destino == 'C':
                return self.valor
        elif self.unidad == 'F':
            if destino == 'C':
                return (self.valor - 32) * 5/9
            elif destino == 'K':
                return ((self.valor - 32) * 5/9) + 273.15
            elif destino == 'F':
                return self.valor
        elif self.unidad == 'K':
            if destino == 'C':
                return self.valor - 273.15
            elif destino == 'F':
                return ((self.valor - 273.15) * 9/5) + 32
            elif destino == 'K':
                return self.valor
        else:
            return ValueError("Unidad no reconocida.")

conversion_C_K = Temperatura(30, 'C')
print(conversion_C_K.conversion_unidad('F'))
print(conversion_C_K.conversion_unidad('K'))