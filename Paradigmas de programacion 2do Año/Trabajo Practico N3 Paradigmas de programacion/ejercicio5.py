# Nombre alumno: Franco Genaro Reyes
class Empleado:
    def __init__(self, nombre, horas_trabajadas, tarifa_hora):
        self.nombre = nombre
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora

    def calcular_salario(self):
        return self.horas_trabajadas * self.tarifa_hora

    def mostrar_info(self):
        print(f'Empleado: {self.nombre}')
        print(f'Horas trabajadas: {self.horas_trabajadas}')
        print(f'Tarifa por hora: ${self.tarifa_hora}')
        print(f'Salario total: ${self.calcular_salario()}')

empleado1 = Empleado("Franco Reyes", 40, 1500)
empleado1.mostrar_info()