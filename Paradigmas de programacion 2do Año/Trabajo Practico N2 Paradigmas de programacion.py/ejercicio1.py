# Nombre alumno: Franco Genaro Reyes
class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura
    
    def calculo_area(self):
        return self.base * self.altura
    
    def calculo_perimetro(self):
        return 2*(self.base + self.altura)
    
rectangulo1 = Rectangulo(5, 14)
print(f'El area del rectangulo1 es: {rectangulo1.calculo_area()} y el perimetro es {rectangulo1.calculo_perimetro()}')