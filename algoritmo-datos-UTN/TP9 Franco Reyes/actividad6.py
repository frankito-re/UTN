def leer_pacientes(archivo):
    pacientes = []
    with open(archivo, 'r') as file:
        for linea in file:
            # Asegurarse de que la línea no esté vacía
            if linea.strip():
                # Separar los datos por comas y eliminamos espacios innecesarios
                partes = linea.split(',')
                if len(partes) == 4:  # Asegurarse de que hay 4 partes
                    apellido = partes[0].strip()
                    nombre = partes[1].strip()
                    edad = partes[2].strip()
                    obra_social = partes[3].strip()
                    # Convertir la edad a entero para poder ordenar por ella
                    pacientes.append((apellido, nombre, int(edad), obra_social))
    return pacientes

# Función para escribir los pacientes ordenados en un nuevo archivo
def escribir_pacientes_por_edad(pacientes, archivo):
    with open(archivo, 'w') as file:
        for paciente in pacientes:
            # Escribir los datos del paciente en formato correcto
            file.write(f"{paciente[0]}, {paciente[1]}, {paciente[2]}, {paciente[3]}\n")

# Leer los datos del archivo 'pacientes.txt'
pacientes = leer_pacientes('pacientes.txt')

# Ordenar la lista de pacientes por edad (tercer elemento de cada tupla)
pacientes_ordenados = sorted(pacientes, key=lambda x: x[2])

# Escribir los pacientes ordenados en un nuevo archivo 'pacientes_por_edad.txt'
escribir_pacientes_por_edad(pacientes_ordenados, 'pacientes_por_edad.txt')

# Mostrar los pacientes ordenados por consola
print("Pacientes ordenados por edad:")
for paciente in pacientes_ordenados:
    print(f"{paciente[0]}, {paciente[1]}, {paciente[2]}, {paciente[3]}")