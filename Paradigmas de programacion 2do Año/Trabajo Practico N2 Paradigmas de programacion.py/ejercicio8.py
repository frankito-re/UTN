# Nombre alumno: Franco Genaro Reyes

# Mazo de Cartas. Crear una clase llamada MazoCartas, que representara un mazo de
# 52 cartas de poker. Debera usar internamente otra clase, que tambien debera crear llamada Carta que modelara una carta de poker propiamente dicha.
# a) La clase MazoCartas tendra un metodo repartir que robara una carta del mazo,
# eliminandola de este.
# b) Un metodo llamado barajar que mezcle nuevamente las cartas y se asegure que esten
# las 52.
# c) La clase Carta, ademas, debera tener los siguientes atributos: palo (Corazones, Diamantes, Treboles, Picas) y valor. (A,2,3,4,5,6,7,8,9,10,J,Q,K)
import random

class MazoCartas:
    class Carta:
        def __init__(self, valor_carta, nombre_palo):
            self.valor_carta = valor_carta
            self.nombre_palo = nombre_palo
    
    def __init__(self):
        self.valores_cartas= ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.palos = ['Corazones', 'Diamantes', 'Treboles', 'Picas']
        self.cartas = [MazoCartas.Carta(valor, palo) for palo in self.palos for valor in self.valores_cartas]

    def repartir(self):
        return self.cartas.pop()

    def barajar(self):
        self.__init__()
        random.shuffle(self.cartas)
    
    def mostrar_mazo(self):
        for carta in self.cartas:
            print(f'Carta: {carta.valor_carta} de {carta.nombre_palo}')
    
mazo_cartas = MazoCartas()
mazo_cartas.mostrar_mazo()