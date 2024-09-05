# 6. Realizar un programa para calcular la liquidación de sueldo:
# a. Crear una clase llamada “Empleado”
# b. La clase debe contener los atributos: nombre, horas-trabajadas y tarifa-hora.
# c. Crear el método: calculo-salario.
# d. Pedir al usuario que ingrese todos los empleados que son parte de la empresa en una lista para
# que luego el programa calcule el sueldo que le corresponde cobrar en función de las horas
# trabajadas y el valor de la hora trabajada para cada empleado que figure en la lista. Mostrar en
# pantalla el nombre del empleado y el sueldo que le corresponde cobrar.

class Empleado:
    def __init__(self, nombre, horas_trabajadas, tarifa_hora):
        self.nombre = nombre
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora
    
    def calculo_salario(self):
        return self.tarifa_hora * self.horas_trabajadas

def ingresar_empleados():
    empleados = []
    while True:
        nombre = input("Ingrese el nombre del empleado (o escriba 'salir' para terminar): ")
        if nombre.lower() == 'salir':
            break
        try:
            horas_trabajadas = float(input(f"Ingrese las horas trabajadas por {nombre}: "))
            tarifa_hora = float(input(f"Ingrese la tarifa por hora de {nombre}: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
        
        empleado = Empleado(nombre, horas_trabajadas, tarifa_hora)
        empleados.append(empleado)
    
    return empleados

def mostrar_sueldos(empleados):
    print("\nLiquidación de sueldos:")
    for empleado in empleados:
        sueldo = empleado.calculo_salario()
        print(f"{empleado.nombre}: ${sueldo:.2f}")

empleados = ingresar_empleados()
mostrar_sueldos(empleados)
