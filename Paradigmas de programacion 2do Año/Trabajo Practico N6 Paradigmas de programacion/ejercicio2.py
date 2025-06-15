# Nombre alumno: Franco Genaro Reyes
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Asegurate de poner tu contraseña si es necesario
    database="bd_empresa"
)

cursor = conexion.cursor()

# Insertar CLIENTE
print("\\n--- Ingresar datos del CLIENTE ---")
id_cliente = int(input("ID Cliente: "))
apellido = input("Apellido: ")
nombre = input("Nombre: ")
telefono = int(input("Teléfono (10 dígitos): "))
domicilio = input("Domicilio: ")
email = input("Email: ")
activo = input("¿Activo? (S/N): ")

query_cliente = "INSERT INTO clientes (id_cliente, apellido, nombre, telefono, domicilio, email, activo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val_cliente = (id_cliente, apellido, nombre, telefono, domicilio, email, activo)
cursor.execute(query_cliente, val_cliente)
conexion.commit()
print("Cliente insertado correctamente.")

# Insertar PROVEEDOR
print("\\n--- Ingresar datos del PROVEEDOR ---")
id_proveedor = int(input("ID Proveedor: "))
razon_social = input("Razón Social: ")
telefono = int(input("Teléfono (10 dígitos): "))
domicilio = input("Domicilio: ")
email = input("Email: ")
contacto = input("Contacto: ")
activo = input("¿Activo? (S/N): ")

query_proveedor = "INSERT INTO proveedores (id_proveedor, razon_social, telefono, domicilio, email, contacto, activo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val_proveedor = (id_proveedor, razon_social, telefono, domicilio, email, contacto, activo)
cursor.execute(query_proveedor, val_proveedor)
conexion.commit()
print("Proveedor insertado correctamente.")

# Insertar ARTICULO
print("\\n--- Ingresar datos del ARTÍCULO ---")
id_articulo = int(input("ID Artículo: "))
descripcion = input("Descripción: ")
precio_compra = float(input("Precio de compra: "))
precio_venta = float(input("Precio de venta: "))
stock = int(input("Stock: "))
id_proveedor_fk = int(input("ID Proveedor (FK): "))
activo = input("¿Activo? (S/N): ")

query_articulo = "INSERT INTO articulos (id_articulo, descripcion, precio_compra, precio_venta, stock, id_proveedor, activo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
val_articulo = (id_articulo, descripcion, precio_compra, precio_venta, stock, id_proveedor_fk, activo)
cursor.execute(query_articulo, val_articulo)
conexion.commit()
print("Artículo insertado correctamente.")

# Cierre de conexión
cursor.close()
conexion.close()
