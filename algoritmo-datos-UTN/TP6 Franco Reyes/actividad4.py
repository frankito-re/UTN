# Se requiere un programa que modele el concepto de un planeta del sistema solar. Un planeta tiene los siguientes atributos:
# a. Un nombre de tipo String con valor inicial de null.
# b. Cantidad de satélites de tipo int con valor inicial de cero.
# c. Masa en kilogramos de tipo float con valor inicial de cero
# d. Volumen en kilómetros cúbicos de tipo float con valor inicial de cero.
# e. Diámetro en kilómetros de tipo int con valor inicial de cero.
# f. Distancia media al Sol en millones de kilómetros, de tipo int con valor inicial de cero.
# g. Tipo de planeta de acuerdo con su tamaño, de tipo string con valor inicial null.
# h. Observable a simple vista, de tipo booleano con valor inicial false.

# La clase debe incluir los siguientes métodos:
# a. La clase debe tener un constructor que inicialice los valores de sus respectivos atributos.
# b. Definir un método que imprima en pantalla los valores de los atributos de un planeta.
# c. Calcular la densidad un planeta, como el cociente entre su masa y su volumen.
# d. Determinar si un planeta del sistema solar se considera exterior.
# Un planeta exterior está situado más allá del cinturón de asteroides. El cinturón de asteroides
# se encuentra entre 2.1 y 3.4 UA. Una unidad astronómica (UA) es la distancia entre la Tierra y
# el Sol=149597870 Km.
# Se deben crear dos planetas y mostrar los valores de sus atributos en pantalla. Además, se debe
# imprimir la densidad de cada planeta y si el planeta es un planeta exterior del sistema solar.

class Planeta:
    def __init__(self):
        # Atributos con valores iniciales
        self.nombre = None  # Tipo String, valor inicial null
        self.cantidad_satelites = 0  # Tipo int, valor inicial 0
        self.masa = 0.0  # Tipo float, valor inicial 0
        self.volumen = 0.0  # Tipo float, valor inicial 0
        self.diametro = 0  # Tipo int, valor inicial 0
        self.distancia_media_sol = 0  # Tipo int, valor inicial 0
        self.tipo_planeta = None  # Tipo String, valor inicial null
        self.observable_a_simple_vista = False  # Tipo booleano, valor inicial False

    def show_info(self):
        print(f"Nombre: {self.nombre}")
        print(f"Cantidad de satélites: {self.cantidad_satelites}")
        print(f"Masa (kg): {self.masa}")
        print(f"Volumen (km³): {self.volumen}")
        print(f"Diámetro (km): {self.diametro}")
        print(f"Distancia media al Sol (millones de km): {self.distancia_media_sol}")
        print(f"Tipo de planeta: {self.tipo_planeta}")
        print(f"Observable a simple vista: {'Sí' if self.observable_a_simple_vista else 'No'}")
        
    def planet_density(self):
        if self.volumen > 0:
            densidad = self.masa / self.volumen
            print(f'La densidad del planeta es: {densidad} kg/km³')
        else:
            print('El volumen debe ser mayor que cero para calcular la densidad.')
        
    def is_extern(self):
        if self.distancia_media_sol > 228:
            return True
        else:
            return False


# Creando el primer planeta: Marte
marte = Planeta()
marte.nombre = "Marte"
marte.cantidad_satelites = 2
marte.masa = 6.4171e23
marte.volumen = 1.6318e11
marte.diametro = 6779
marte.distancia_media_sol = 228
marte.tipo_planeta = "Terrestre"
marte.observable_a_simple_vista = True

# Mostrando información y calculando la densidad
marte.show_info()
marte.planet_density()
print(f"¿Es Marte un planeta exterior? {'Sí' if marte.is_extern() else 'No'}\n")

# Creando el segundo planeta: Júpiter
jupiter = Planeta()
jupiter.nombre = "Júpiter"
jupiter.cantidad_satelites = 79
jupiter.masa = 1.898e27
jupiter.volumen = 1.43128e15
jupiter.diametro = 139820
jupiter.distancia_media_sol = 778
jupiter.tipo_planeta = "Gaseoso"
jupiter.observable_a_simple_vista = True

# Mostrando información y calculando la densidad
jupiter.show_info()
jupiter.planet_density()
print(f"¿Es Júpiter un planeta exterior? {'Sí' if jupiter.is_extern() else 'No'}")
