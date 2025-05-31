# Nombre alumno: Franco Genaro Reyes
def verificar_contrasena(funcion_original):
    def wrapper():
        contrasena = input("Ingrese la contraseña: ")
        if contrasena == "secreta123":
            return funcion_original()
        else:
            print("Contraseña incorrecta. Acceso denegado.")
    return wrapper

@verificar_contrasena
def mostrar_info_confidencial():
    print("Acceso concedido. Información secreta mostrada.")

mostrar_info_confidencial()