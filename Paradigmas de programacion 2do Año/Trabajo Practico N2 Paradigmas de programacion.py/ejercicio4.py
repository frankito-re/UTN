# Nombre alumno: Franco Genaro Reyes
class Persona:
    def __init__(self, nombre, peso, altura):
        self.nombre = nombre
        self.peso = peso
        self.altura = altura
    
    def calcular_imc(self):
        return self.peso/(self.altura**2)
    
persona1 = Persona('Franco', 71, 1.71)

print(f'El IMC de Franco es: {persona1.calcular_imc()}')