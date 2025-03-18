class Nodo:
    def __init__(self, dato):
        self.dato = dato  
        self.siguiente = None  
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  
    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:  
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente: 
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo  
    def contar_nodos(self):
        contador = 0
        actual = self.cabeza
        while actual:  
            contador += 1
            actual = actual.siguiente  
        return contador
    def posicion_nodo(self, valor):
        posicion = 1  
        actual = self.cabeza
        while actual:
            if actual.dato == valor:
                return posicion  
            actual = actual.siguiente
            posicion += 1
        return -1  
# Creación de la lista enlazada
lista = ListaEnlazada()
# Agregamos algunos nodos
lista.agregar(10)
lista.agregar(20)
lista.agregar(30)
# Valor ingresado por el usuario
valor_buscado = int(input("Ingrese el valor a buscar: "))
# Buscar la posición del nodo con ese valor
posicion = lista.posicion_nodo(valor_buscado)
if posicion != -1:
    print(f"El nodo con el valor {valor_buscado} está en la posición {posicion}.")
else:
    print(f"El nodo con el valor {valor_buscado} no se encuentra en la lista.")