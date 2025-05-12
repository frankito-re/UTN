# Nombre alumno: Franco Genaro Reyes
class Personaje:
    def __init__(self, nombre, clase):
        self.nombre = nombre
        self.clase = clase
        self.nivel = 1
        self.salud = 100
        self.fuerza = 10
        self.defensa = 5
        self.inventario = []

    def atacar(self, otro):
        daño = self.fuerza - otro.defensa
        if daño < 0:
            daño = 0
        print(f'{self.nombre} ataca a {otro.nombre} causando {daño} de daño.')
        otro.recibir_daño(daño)

    def recibir_daño(self, puntos):
        self.salud -= puntos
        if self.salud < 0:
            self.salud = 0
        print(f'{self.nombre} recibió {puntos} de daño. Salud restante: {self.salud}')

    def curarse(self, puntos):
        self.salud += puntos
        if self.salud > 100:
            self.salud = 100
        print(f'{self.nombre} se curó {puntos} puntos. Salud actual: {self.salud}')

    def subir_nivel(self):
        self.nivel += 1
        self.fuerza += 5
        self.salud += 20
        print(f'{self.nombre} subió a nivel {self.nivel}')

    def agregar_item(self, item):
        self.inventario.append(item)
        print(f'{self.nombre} agregó {item} al inventario.')

    def mostrar_estado(self):
        print(f'{self.nombre} | Clase: {self.clase} | Nivel: {self.nivel} | Salud: {self.salud} | Fuerza: {self.fuerza} | Defensa: {self.defensa}')
        print('Inventario:', ', '.join(self.inventario) if self.inventario else 'Vacío')

p1 = Personaje('Arthas', 'Guerrero')
p2 = Personaje('Morgana', 'Hechicera')

p1.mostrar_estado()
p1.agregar_item('Espada de fuego')
p1.atacar(p2)
p2.curarse(15)
p1.subir_nivel()