# Nombre alumno: Franco Genaro Reyes
class Carrito:
    def __init__(self):
        self.items = []

    def agregar_item(self, nombre, precio, cantidad):
        encontrado = False
        for item in self.items:
            if item['nombre'] == nombre:
                item['cantidad'] += cantidad
                encontrado = True
        if not encontrado:
            self.items.append({'nombre': nombre, 'precio': precio, 'cantidad': cantidad})

    def quitar_item(self, nombre):
        nueva_lista = []
        for item in self.items:
            if item['nombre'] != nombre:
                nueva_lista.append(item)
        self.items = nueva_lista

    def costo_total(self):
        total = 0
        for item in self.items:
            total += item['precio'] * item['cantidad']
        return total

    def tiene_envio_gratis(self):
        return self.costo_total() >= 10000

    def mostrar_carrito(self):
        print('\nCarrito de compras:')
        for item in self.items:
            print(f'{item['nombre']} - ${item['precio']} x {item['cantidad']}')
        print(f'Total: ${self.costo_total()}')
        if self.tiene_envio_gratis():
            print('Envío gratis incluido')
        else:
            print('No tiene envío gratis')