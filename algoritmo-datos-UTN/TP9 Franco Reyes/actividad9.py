class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
    
    def __repr__(self):
        return f"{self.nombre}: ${self.precio}"

def insertion_sort(lista):
    for i in range(1, len(lista)):
        key = lista[i]
        j = i - 1
    
        while j >= 0 and key.precio < lista[j].precio:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = key

# Crear una lista de productos
productos = [
    Producto("Producto A", 30.50),
    Producto("Producto B", 10.99),
    Producto("Producto C", 20.00),
    Producto("Producto D", 15.75),
    Producto("Producto E", 25.00)
]

insertion_sort(productos)

# Imprimir los productos
for producto in productos:
    print(producto)