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
    def eliminar_penultimo(self):
        if not self.cabeza or not self.cabeza.siguiente:
            print("No se puede eliminar el penúltimo nodo: la lista tiene menos de dos nodos.")
            return
        actual = self.cabeza
        # Si la lista tiene exactamente dos nodos
        if not actual.siguiente.siguiente:
            # En este caso, eliminamos el primer nodo, ya que es el penúltimo
            self.cabeza = self.cabeza.siguiente
            return
        # Recorremos la lista hasta llegar al nodo anterior al penúltimo
        while actual.siguiente.siguiente.siguiente:
            actual = actual.siguiente
        # Eliminamos el penúltimo nodo apuntando al último nodo
        actual.siguiente = actual.siguiente.siguiente
    def mostrar(self):
        """Método para mostrar la lista enlazada."""
        actual = self.cabeza
        while actual:
            print(actual.dato, end=" -> ")
            actual = actual.siguiente
        print("None")
# Creación de la lista enlazada
lista = ListaEnlazada()
# Agregamos algunos nodos
lista.agregar(10)
lista.agregar(20)
lista.agregar(30)
lista.agregar(40)
lista.agregar(50)
# Mostramos la lista original
print("Lista original:")
lista.mostrar()
# Eliminamos el penúltimo nodo
lista.eliminar_penultimo()
# Mostramos la lista después de eliminar el penúltimo nodo
print("Lista después de eliminar el penúltimo nodo:")
lista.mostrar()