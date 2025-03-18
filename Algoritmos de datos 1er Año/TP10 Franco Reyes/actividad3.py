# Paso 1: Lista de alumnos que se presentaron al examen
alumnos = ["Ana", "Carlos", "Beatriz", "Daniel", "Elena", "Francisco", "Gabriela", "Hugo", "Irene", "Juan"]
# Mostrar la lista de alumnos para referencia
print("Alumnos que se presentaron al examen:", alumnos)
# Paso 2: Pedir al usuario el nombre de un alumno
nombre_buscar = input("Introduce el nombre del alumno que quieres buscar: ")
# Paso 3: Búsqueda secuencial
if nombre_buscar in alumnos:
    print(f"El alumno {nombre_buscar} se presentó al examen.")
else:
    print(f"El alumno {nombre_buscar} no se presentó al examen.")