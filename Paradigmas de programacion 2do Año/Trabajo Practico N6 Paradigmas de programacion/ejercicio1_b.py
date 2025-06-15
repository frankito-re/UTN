# Nombre alumno: Franco Genaro Reyes
import mysql.connector as mysql

conexion = mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="bd_familia"
)

cursor = conexion.cursor()

id = int(input("Ingrese el ID del amigo (número): "))
nombre = input("Ingrese el nombre: ")
apellido = input("Ingrese el apellido: ")
telefono = input("Ingrese el teléfono: ")
domicilio = input("Ingrese el domicilio: ")
correo = input("Ingrese el correo electrónico: ")
fec_nac = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
estado = input("Ingrese el estado (1 para activo, 0 para inactivo): ")

consulta = """INSERT INTO amigos (id, nombre, apellido, telefono, domicilio, correo, fec_nac, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

datos = (id, nombre, apellido, telefono, domicilio, correo, fec_nac, estado)
cursor.execute(consulta, datos)
conexion.commit()

print("Registro insertado con éxito en tabla 'amigos'.")

conexion.close()