def simular_atencion():
    # Crear la cola de pacientes como una lista de tuplas (nombre, tiene_obra_social)
    cola_pacientes = [
        ("Juan", True),
        ("María", False),
        ("Pedro", True),
        ("Ana", False)
    ]

    # Contador de pacientes con obra social
    pacientes_con_obra_social = 0

    # Atender a los pacientes
    while cola_pacientes:
        # Remover el primer paciente de la cola
        nombre, tiene_obra_social = cola_pacientes.pop(0)
        print(f"Atendiendo a {nombre}")

        # Verificar si tiene obra social
        if tiene_obra_social:
            pacientes_con_obra_social += 1

    print(f"Total de pacientes con obra social: {pacientes_con_obra_social}")

# Ejecutar la simulación
simular_atencion()