# Nombre alumno: Franco Genaro Reyes
def convertidor_mayusculas(f_a_decorar):
    def wrapper():
        resultado = f_a_decorar()
        return resultado.upper()
    return wrapper

@convertidor_mayusculas
def obtener_texto():
    return 'esto es un mensaje en minúsculas'

print(obtener_texto())