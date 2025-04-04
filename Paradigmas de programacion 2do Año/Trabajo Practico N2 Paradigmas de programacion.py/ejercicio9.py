import random

class Heroe:
    class Inventario:
        def __init__(self):
            self.elementos_de_heroe = []
            
    def __init__(self, nombre):
        self.cantidad_vida = 100
        self.nivel_magia = 1
        self.daño = 10
        self.prob_critico = 0.25
        self.multiplicador_critico = 2
        self.hambre = 100
        self.nombre = nombre
        self.inventario = Heroe.Inventario()
        self.objetos_en_uso = []
        print(f'El heroe {self.nombre} ha sido creado')

    def atacar(self):
        if random.random() < self.prob_critico:
            print("¡Golpe crítico!")
            return int(self.daño * self.multiplicador_critico)
        else:
            return self.daño

    def tomar_elemento_despensa(self, elemento, despensa):
        if elemento in despensa:
            despensa.remove(elemento)
            self.inventario.elementos_de_heroe.append(elemento)
            print(f"{self.nombre} ha tomado {elemento} de la despensa.")
        else:
            print(f"El item {elemento} no está disponible en la despensa.")
        print(f'Elementos restantes en la despensa: {despensa}')

    def usar_elemento(self, elemento):
        if elemento in self.inventario.elementos_de_heroe:
            self.inventario.elementos_de_heroe.remove(elemento)
            self.objetos_en_uso.append(elemento)
            print(f'{self.nombre} está usando el item {elemento}')
        else:
            print(f'El item {elemento} no se encuentra en el inventario')
        
    def dejar_elemento(self, elemento):
        if elemento in self.objetos_en_uso:
            self.objetos_en_uso.remove(elemento)
            self.inventario.elementos_de_heroe.append(elemento)
            print(f'{self.nombre} dejó de usar el item {elemento}')
        else:
            print(f'{self.nombre} no está usando el item {elemento}')

despensa = ["Pocion", "Flechas", "Escudo"]
heroe1 = Heroe('Franco')
heroe1.tomar_elemento_despensa('Pocion', despensa)
heroe1.usar_elemento('Pocion')
heroe1.dejar_elemento_en_inventario()
heroe1.tomar_elemento_despensa('Escudo', despensa)
heroe1.usar_elemento('Escudo')
heroe1.dejar_elemento_en_inventario()