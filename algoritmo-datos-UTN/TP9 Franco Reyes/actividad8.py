def ordenamiento_seleccion(estudiantes):
    
    for i in range(len(estudiantes)):
        
        max_idx = i
        for j in range(i + 1, len(estudiantes)):
            if estudiantes[j]['calificacion'] > estudiantes[max_idx]['calificacion']:
                max_idx = j
        
        
        estudiantes[i], estudiantes[max_idx] = estudiantes[max_idx], estudiantes[i]
    
    return estudiantes

# Ejemplo de uso
estudiantes = [
    {"nombre": "Ana", "calificacion": 85},
    {"nombre": "Carlos", "calificacion": 90},
    {"nombre": "Beatriz", "calificacion": 78},
    {"nombre": "Lucía", "calificacion": 92},
    {"nombre": "Javier", "calificacion": 88}
]

estudiantes_ordenados = ordenamiento_seleccion(estudiantes)

# Imprimir la lista ordenada
print("Lista de estudiantes ordenada por calificación (de mayor a menor):")
for estudiante in estudiantes_ordenados:
    print(f"Nombre: {estudiante['nombre']}, Calificación: {estudiante['calificacion']}")