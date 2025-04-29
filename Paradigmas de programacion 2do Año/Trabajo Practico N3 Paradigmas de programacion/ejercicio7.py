# Nombre alumno: Franco Genaro Reyes
class Estudiante:
    def __init__(self, nombre, dni, edad, carrera, materias, promedio, aprobado):
        self.nombre = nombre
        self.dni = dni
        self.edad = edad
        self.carrera = carrera
        self.materias = materias
        self.promedio = promedio
        self.aprobado = aprobado
        
    # Los metodos que deberia tener esta clase Estudiante
    # - agregar_materia(materia)     # agregar una materia a su lista
    # - actualizar_promedio(nota)    # calcular nuevo promedio
    # - mostrar_info()               # imprime todos los datos del estudiante
    # - esta_aprobado()              # retorna True si el promedio supera cierto valor