import os

# Nombre del archivo
archivo_ventas = 'ventas.txt'

def agregar_producto(nombre, cantidad, precio):
    with open(archivo_ventas, 'a') as archivo:
        archivo.write(f"{nombre},{cantidad},{precio}\n")
    print(f"Producto '{nombre}' agregado.")

def consultar_productos():
    if not os.path.exists(archivo_ventas):
        print("No hay productos registrados.")
        return
    with open(archivo_ventas, 'r') as archivo:
        lineas = archivo.readlines()
        if not lineas:
            print("No hay productos registrados.")
            return
        for linea in lineas:
            nombre, cantidad, precio = linea.strip().split(',')
            print(f"Producto: {nombre}, Cantidad vendida: {cantidad}, Precio: {precio}")

def actualizar_producto(nombre, nueva_cantidad, nuevo_precio):
    if not os.path.exists(archivo_ventas):
        print("No hay productos registrados.")
        return
    actualizado = False
    with open(archivo_ventas, 'r') as archivo:
        lineas = archivo.readlines()
    with open(archivo_ventas, 'w') as archivo:
        for linea in lineas:
            nombre_actual, cantidad, precio = linea.strip().split(',')
            if nombre_actual == nombre:
                archivo.write(f"{nombre},{nueva_cantidad},{nuevo_precio}\n")
                actualizado = True
            else:
                archivo.write(linea)
    if actualizado:
        print(f"Producto '{nombre}' actualizado.")
    else:
        print(f"Producto '{nombre}' no encontrado.")

def eliminar_producto(nombre):
    if not os.path.exists(archivo_ventas):
        print("No hay productos registrados.")
        return
    eliminado = False
    with open(archivo_ventas, 'r') as archivo:
        lineas = archivo.readlines()
    with open(archivo_ventas, 'w') as archivo:
        for linea in lineas:
            nombre_actual, cantidad, precio = linea.strip().split(',')
            if nombre_actual == nombre:
                eliminado = True
            else:
                archivo.write(linea)
    if eliminado:
        print(f"Producto '{nombre}' eliminado.")
    else:
        print(f"Producto '{nombre}' no encontrado.")

def calcular_venta_total():
    if not os.path.exists(archivo_ventas):
        print("No hay productos registrados.")
        return
    total = 0
    with open(archivo_ventas, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            nombre, cantidad, precio = linea.strip().split(',')
            total += int(cantidad) * float(precio)
    print(f"Venta total: {total}")

def calcular_venta_por_producto(nombre):
    if not os.path.exists(archivo_ventas):
        print("No hay productos registrados.")
        return
    total = 0
    encontrado = False
    with open(archivo_ventas, 'r') as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            nombre_actual, cantidad, precio = linea.strip().split(',')
            if nombre_actual == nombre:
                total += int(cantidad) * float(precio)
                encontrado = True
    if encontrado:
        print(f"Venta total para '{nombre}': {total}")
    else:
        print(f"Producto '{nombre}' no encontrado.")

def salir_y_borrar_archivo():
    if os.path.exists(archivo_ventas):
        os.remove(archivo_ventas)
        print(f"Archivo '{archivo_ventas}' borrado.")
    else:
        print("No hay archivo que borrar.")
    print("Saliendo del programa.")
    exit()

def mostrar_menu():
    print("\n--- Menú de Gestión de Ventas ---")
    print("1. Añadir producto")
    print("2. Consultar productos")
    print("3. Actualizar producto")
    print("4. Eliminar producto")
    print("5. Calcular venta total")
    print("6. Calcular venta por producto")
    print("7. Salir y borrar archivo")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre = input("Nombre del producto: ")
            cantidad = input("Cantidad vendida: ")
            precio = input("Precio: ")
            agregar_producto(nombre, cantidad, precio)
        elif opcion == '2':
            consultar_productos()
        elif opcion == '3':
            nombre = input("Nombre del producto a actualizar: ")
            nueva_cantidad = input("Nueva cantidad vendida: ")
            nuevo_precio = input("Nuevo precio: ")
            actualizar_producto(nombre, nueva_cantidad, nuevo_precio)
        elif opcion == '4':
            nombre = input("Nombre del producto a eliminar: ")
            eliminar_producto(nombre)
        elif opcion == '5':
            calcular_venta_total()
        elif opcion == '6':
            nombre = input("Nombre del producto para calcular la venta: ")
            calcular_venta_por_producto(nombre)
        elif opcion == '7':
            salir_y_borrar_archivo()
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main()