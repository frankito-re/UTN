# Definición de la clase Nodo
class Nodo:
    def __init__(self, dato):
        self.dato = dato 
        self.siguiente = None  
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  
    def agregar(self, dato):
        """Método para agregar un nodo al final de la lista."""
        nuevo_nodo = Nodo(dato)
        if not self.cabeza:  
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:  
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo 
    def contar_nodos(self):
        """Método para contar el número de nodos en la lista."""
        contador = 0
        actual = self.cabeza
        while actual:  
            contador += 1
            actual = actual.siguiente  
        return contador
# Creación de la lista enlazada
lista = ListaEnlazada()
# Agregamos algunos nodos
lista.agregar(10)
lista.agregar(20)
lista.agregar(30)
# Contamos la cantidad de nodos
print("Cantidad de nodos:", lista.contar_nodos())