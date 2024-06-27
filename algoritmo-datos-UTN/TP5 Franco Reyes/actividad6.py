def contar_nombres_con_letra(nombres, letra):
    if not nombres:
        return 0
    else:
        if nombres[0].startswith(letra):
            return 1 + contar_nombres_con_letra(nombres[1:], letra)
        else:
            return contar_nombres_con_letra(nombres[1:], letra)

nombres = ["Ana", "Andrés", "Beatriz", "Alberto", "Carlos"]
letra = "A"
cantidad = contar_nombres_con_letra(nombres, letra)
print(f"La cantidad de nombres que empiezan con '{letra}' es: {cantidad}")
