# Shelter de Mascotas.
# Se desea desarrollar un sistema para un Shelter de mascotas (Shelter: refugio temporal para mascotas que se espera sean adoptadas). Los animales que este shelter cuida
# temporalmente y trata de ubicar en adopcion son: perros, gatos, conejos, canarios,
# tortugas y peces.
# Implementar una clase Animal que tendra los siguientes atributos genericos para
# cualquiera de los animales que interesaran en este programa: raza, nombre, color,
# edad, estado de salud, genero.
# El estado de salud, debera ser implementado como un atributo que solo puede tomar
# uno de los valores posibles de una lista de opciones, cuyos valores seran diferentes
# segun el tipo de animal, pues peces no tienen los mismos problemas que los perros
# por ejemplo.
class Animal:
    def __init__(self, raza, nombre, color, edad, estado_de_salud, genero):
        self.raza = raza
        self.nombre = nombre
        self.color = color
        self.edad = edad
        self.genero = genero
        self.estado_de_salud = None
        self.estados_salud_posibles = []
        self.validar_estado_de_salud(estado_de_salud)

    def validar_estado_de_salud(self, estado):
        if estado in self.estados_salud_posibles:
            self.estado_de_salud = estado
        else:
            return 'Ese tipo de salud no esta disponible'

# Para animales con patas, el estado de salud podria contar con los siguientes valores
# posibles: sano, enfermo cronico, cojo, debil.
class Perro(Animal):
    def __init__(self, raza, nombre, color, edad, estado_de_salud, genero, agresivo):
        super().__init__(raza, nombre, color, edad, estado_de_salud, genero)
        self.estados_salud_posibles = ['sano', 'enfermo cronico', 'cojo', 'debil']
        self.agresivo = agresivo
        
perro1 = Perro()
perro1=Perro("Beagle", "Piku", "Tricolor", 8, "sano", "Hembra")
    
# Analice bien los atributos que podrian hacer falta. Disene para los peces y las aves,
# sus atributos. El metodo adoptar() no es implementado en la clase Padre Animal,
# sino en cada hijo. Determine si le hara falta un atributo adoptado (si/no) en el
# Animal.
# Luego, cuando ya haya disenado e implementado las clases, el siguiente paso sera,
# crear un programa principal, para la administracion de los animales en el Shelter.
# Suponga que al Shelter han llegado 2 conejos nuevos. Y que ya habia 3 perros, un
# gato, 5 peces. Simule ahora como seria el proceso de adopcion para 1 conejo y el
# gato, ademas de un perro, siempre y cuando no sea agresivo y pueda estar con ninos.