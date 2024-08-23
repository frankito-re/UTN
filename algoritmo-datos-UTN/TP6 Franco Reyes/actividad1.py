# Crear una clase llamada Alumno que tenga como atributo el nombre y la nota de alumno. Definir los
# métodos para inicializar sus atributos, imprimirlos y mostrar un mensaje con el resultado de la nota y si
# ha aprobado o no.

class Alumno:
    def __init__(self, student_name, student_mark):
    # Declaro los atributos de la clase y con sus respectivos parametros anexados
        self.student_mark = student_mark 
        self.student_name = student_name
        # Aqui use self para que mis atributos solo pertenezcan a las propias instancias
        
    def decide_approved(self):
        # Ahora uso self.student_mark para acceder al atributo de la instancia
        if self.student_mark < 6:
            print(f'El alumno {self.student_name} está desaprobado')
        else:
            print(f'El alumno {self.student_name} está aprobado')
            
# Voy a crear un objeto/instancia para que se inicialice los atributos
alumno1 = Alumno('Franco', 10)
alumno1.decide_approved()

