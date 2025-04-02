# Heroe Crear una clase llamada Heroe, que representara un guerrero de un juego arcade
# en 2D. Debera usar internamente otra clase, que tambien debera crear llamada Inventario
# que modelara la mochila o inventario del guerrero. En el programa principal habra una
# Despensa, donde habra una lista de elementos disponibles, puede considerar asignarles
# ademas un precio a cada elemento y agregar dinero al Heroe. El Heroe podra tomar elementos de la Despensa, quitandolos de la lista disponible. Tambien podrıa agregar interes
# a dicha lista considerando las cantidades disponibles por elemento y/o su precio. Elementos posibles podrıan ser Pocion, Flechas, Guantes, Escudo, etc
    # a) El Heroe podra realizar las siguientes acciones: tomar un elemento de la despensa
    # (o comprarlo segun la version que ud decida implementar) Podra Usar un elemento
    # que ya tiene, o dejar de usarlo y ponerlo en su mochila. Tendra niveles de sangre o
    # vida, y niveles de magia.
    # b) El Heroe tendra atributos como sangre o vida, nivel de magia, daño, daño crıtico por
    # ejemplo para determinar cuantas posibilidades de hacer mucho daño tiene en cada
    # ataque. Hambre, que lo harıa descansar por ejemplo. Nombre, Guilda. Puede agregar
    # o modificar algunos de los atributos mencionados en pos de diseñar su Heroe.
import random

class Heroe:
    def __init__(self, nombre):
        self.cantidad_vida = 100
        self.nivel_magia = 1
        self.golpe = 1
        self.golpe_critico = 1/4
        self.hambre = 100
        self.nombre = nombre
        
    def atacar(self):
        if random.random() < self.prob_critico:
            print("¡Golpe crítico!")
            return int(self.daño * self.multiplicador_critico)
        else:
            return self.daño
    def tomar_elemento(self):
        pass
    def usar_elemento(self):
        pass
    def dejar_elemento(self):
        pass
    def dejar_elemento_en_inventario(self):
        pass
    
    class Inventario:
        pass
print(random.random())