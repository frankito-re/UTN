# Nombre alumno: Franco Genaro Reyes
class Empleado:
    def __init__(self, nombre, horas_trabajadas, tarifa_hora):
        self.nombre = nombre
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora
    
    def calcular_salario(self):
        return self.tarifa_hora * self.horas_trabajadas
    
empleado1 = Empleado('Franco', 8, 10000)
print(f'El empleado {empleado1.nombre} trabajó {empleado1.horas_trabajadas} y debe cobrar {empleado1.calcular_salario()}')