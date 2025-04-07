# Nombre alumno: Franco Genaro Reyes
class Facturador:
    def __init__(self):
        self.fechafacturacion = ""
        self.nombrecliente = ""
        self.detalle = ""
        self.preciounitario = 0.0
        self.cantidad = 0
        self.preciototal = 0.0

    def facturar_mercaderia(self):
        self.fechafacturacion = input("Ingresá la fecha de facturación: ")
        self.nombrecliente = input("Ingresá el nombre del cliente: ")
        self.detalle = input("Ingresá el detalle del producto: ")
        self.cantidad = int(input("Ingresá la cantidad de productos: "))
        self.preciounitario = float(input("Ingresá el precio unitario del producto: "))

        self.preciototal = self.cantidad * self.preciounitario

    def mostrar_factura_por_pantalla(self):
        print("\nFACTURA")
        print("---------------------------------------------")
        print(f"Fecha: {self.fechafacturacion}")
        print(f"Cliente: {self.nombrecliente}")
        print("---------------------------------------------")
        print(f"Producto: {self.detalle}")
        print(f"Cantidad: {self.cantidad}")
        print(f"Precio unitario: ${self.preciounitario}")
        print("---------------------------------------------")
        print(f"Total a pagar: ${self.preciototal}")
        print("---------------------------------------------")

facturador1 = Facturador()
facturador1.facturar_mercaderia()
facturador1.mostrar_factura_por_pantalla()