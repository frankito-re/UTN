# Crear la clase Triangulo que almacene la longitud de cada uno de sus lados. Deberá contener los
# siguientes métodos:
# a) area(): devuelve el área del triángulo
# b) forma(): indica si se trata de un triángulo equilátero, isósceles o irregular.
# c) perímetro(): devuelve el perímetro del triángulo.
# Se deben crear dos triángulos, mostrar los valores de sus atributos en pantalla, su área, forma y
# perímetro.

class Triangulo:
    # Defino el constructor de la clase y digo, sus atributos van ser una lista, para tener el codigo mas mantenible
    # Los lados de los triangulos deben ser si o si definidos, si no, el codigo se rompe
    def __init__(self, triangle_sides: list):
        self.triangle_sides = triangle_sides
    
    # Defino metodo area()
    def perimetro(self):
        print(f'El area del triangulo es: {sum(self.triangle_sides)}')
    
    # Defino metodo forma()
    def forma(self):
        if self.triangle_sides[0] == self.triangle_sides[1] == self.triangle_sides[2]:
            print("Equilátero")
    
        # Si al menos dos lados son iguales
        elif self.triangle_sides[0] == self.triangle_sides[1] or self.triangle_sides[1] == self.triangle_sides[2]:
            print("Isósceles")
        
        # Si todos los lados son diferentes
        else:
            print("Escaleno")
    
    # Aplico el metodo de area de triangulo: (altura * base) / base
    def area(self):
        print(f'El area del triangulo es: {(self.triangle_sides[0] * self.triangle_sides[1]) / 2}')

print('\nPrimer triangulo:')
triangulo1 = Triangulo([7, 2, 5])
triangulo1.perimetro()
triangulo1.forma()
triangulo1.area()

print('\nSegundo triangulo:')
triangulo2 = Triangulo([14, 98, 17])
triangulo2.perimetro()
triangulo2.forma()
triangulo2.area()
