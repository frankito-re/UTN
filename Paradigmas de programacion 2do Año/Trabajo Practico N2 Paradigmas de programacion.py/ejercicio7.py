# Nombre alumno: Franco Genaro Reyes
class Facturador:
    def __init__(self):
        self.fecha_facturacion = ""
        self.nombre_cliente = ""
        self.detalle = ""
        self.precio_unitario = 0.0
        self.cantidad = 0
        self.precio_total = 0.0

    def facturar_mercaderia(self):
        self.fecha_facturacion = input("Ingresá la fecha de facturación: ")
        self.nombre_cliente = input("Ingresá el nombre del cliente: ")
        self.detalle = input("Ingresá el detalle del producto: ")
        self.cantidad = int(input("Ingresá la cantidad de productos: "))
        self.precio_unitario = float(input("Ingresá el precio unitario del producto: "))

        self.precio_total = self.cantidad * self.precio_unitario

    def mostrar_factura_por_pantalla(self):
        print("\nFACTURA")
        print("---------------------------------------------")
        print(f"Fecha: {self.fecha_facturacion}")
        print(f"Cliente: {self.nombre_cliente}")
        print("---------------------------------------------")
        print(f"Producto: {self.detalle}")
        print(f"Cantidad: {self.cantidad}")
        print(f"Precio unitario: ${self.precio_unitario}")
        print("---------------------------------------------")
        print(f"Total a pagar: ${self.precio_total}")
        print("---------------------------------------------")

facturador1 = Facturador()
facturador1.facturar_mercaderia()
facturador1.mostrar_factura_por_pantalla()