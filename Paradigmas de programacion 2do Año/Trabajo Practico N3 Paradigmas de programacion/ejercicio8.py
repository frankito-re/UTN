# Nombre alumno: Franco Genaro Reyes

# Implemente un programa que permita cargar 6 estudiantes, donde cada uno tiene las
# notas de sus examenes finales. Pueden ser diferentes entre un estudiante y otro, ya que
# cada uno ha rendido o promocionado diferente cantidad de materias. Modifique la clase
# Estudiante si fuese necesario. Realice un programita que le permita cargar 3 estudiantes
# y determine cual es el alumno que sera el abanderado, si lo hubiese.
class Estudiante:
    def __init__(self, notas, nombre):
        self.notas = notas
        self.nombre = nombre

def ingresar_estudiantes(cantidad):
    estudiantes = []
    for i in range(cantidad):
        nombre = str(input('Ingrese el nombre del estudiante: '))
        notas = input(f'Ingrese las notas del alumno {nombre} separadas por espacios: ')
        lista_notas = [float(nota) for nota in notas.split()]
        estudiante = Estudiante(lista_notas, nombre)
        estudiantes.append(estudiante)
        
ingresar_estudiantes(1)