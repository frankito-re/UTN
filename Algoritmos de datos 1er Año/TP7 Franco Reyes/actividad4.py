# 4. Un conductor maneja de un pueblo origen a un pueblo destino, pasando por varios pueblos.
# Una vez en el pueblo destino, el conductor debe regresar a casa por el mismo camino. Muestre
# el camino recorrido tanto de ida como de vuelta.

def recorrido_pueblos():
    pila = []
    
    print("\nRecorrido de ida:")
    for pueblo in pueblos:
        print(pueblo, end=" -> ")
        pila.append(pueblo) 
    print("Destino")
    
    print("\nRecorrido de vuelta:")
    while pila:
        pueblo = pila.pop()
        if pila:
            print(pueblo, end=" -> ")
        else:
            print(pueblo, "Origen")
                
pueblos = ["Pueblo A", "Pueblo B", "Pueblo C", "Pueblo D", "Pueblo Destino"]
recorrido_pueblos()