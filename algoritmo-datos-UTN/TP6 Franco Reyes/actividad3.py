# Crear una clase llamada Persona. Sus atributos son: nombre, apellido, edad y DNI. Construye los
# siguientes métodos para la clase:
# a. Un constructor, donde los datos pueden estar vacíos.
# b. mostrar(): Muestra los datos de la persona.
# c. esMayorDeEdad(): Devuelve un valor lógico indicando si es mayor de edad.
# Se deben crear dos personas y mostrar los valores de sus atributos en pantalla. Y si son mayores o
# menores de edad.

class Persona:
    # a. Un constructor, donde los datos pueden estar vacíos.
    def __init__(self, nombre, apellido, edad, dni):
        self.name = nombre
        self.last_name = apellido
        self.age = edad
        self.dni = dni
    # Ya que la actividad no lo especifica, voy a ahorrar codigo inicializando los metodos aqui, en el constructor
        self.mostrar_datos = self.mostrar()
        self.es_mayor_edad = self.esMayorDeEdad()
    
    # b. mostrar(): Muestra los datos de la persona.
    def mostrar(self):
        print(f'Los datos de la persona son: \nNombre: {self.name}\nApellido: {self.last_name}\nEdad:{self.age}\nDNI: {self.dni}')
        
    # c. esMayorDeEdad(): Devuelve un valor lógico indicando si es mayor de edad.
    def esMayorDeEdad(self):
        print(f'Es mayor de edad: {self.age >= 18}')
        
persona1 = Persona('Franco', 'Reyes', 18, 51238129)