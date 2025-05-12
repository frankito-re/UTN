class Animal:
    def __init__(self, especie, nombre, raza, color, edad, genero, estado_salud):
        self.especie = especie
        self.nombre = nombre
        self.raza = raza
        self.color = color
        self.edad = edad
        self.genero = genero
        self.estado_salud = estado_salud
        self.adoptado = False

    def mostrar_info(self):
        estado = 'Adoptado' if self.adoptado else 'Disponible'
        print(f'{self.nombre} ({self.especie}) - {self.raza}, {self.color}, {self.edad} años, {self.genero}, Salud: {self.estado_salud}, Estado: {estado}')

class Perro(Animal):
    def __init__(self, nombre, raza, color, edad, genero, estado_salud, es_agresivo, bueno_con_niños):
        super().__init__('Perro', nombre, raza, color, edad, genero, estado_salud)
        self.es_agresivo = es_agresivo
        self.bueno_con_niños = bueno_con_niños

    def adoptar(self):
        if not self.es_agresivo and self.bueno_con_niños:
            self.adoptado = True
            return True
        return False

class Gato(Animal):
    def __init__(self, nombre, raza, color, edad, genero, estado_salud):
        super().__init__('Gato', nombre, raza, color, edad, genero, estado_salud)

    def adoptar(self):
        self.adoptado = True
        return True

class Conejo(Animal):
    def __init__(self, nombre, raza, color, edad, genero, estado_salud):
        super().__init__('Conejo', nombre, raza, color, edad, genero, estado_salud)

    def adoptar(self):
        self.adoptado = True
        return True

class Pez(Animal):
    def __init__(self, nombre, raza, color, edad, genero, estado_salud, tipo_agua):
        super().__init__('Pez', nombre, raza, color, edad, genero, estado_salud)
        self.tipo_agua = tipo_agua  # dulce o salada

    def adoptar(self):
        self.adoptado = True
        return True    

class Canario(Animal):
    def __init__(self, nombre, raza, color, edad, genero, estado_salud, plumaje):
        super().__init__('Canario', nombre, raza, color, edad, genero, estado_salud)
        self.plumaje = plumaje  # fuerte o débil

    def adoptar(self):
        self.adoptado = True
        return True

# Crear animales
perros = [
    Perro('Roco', 'Labrador', 'marrón', 4, 'macho', 'sano', False, True),
    Perro('Toby', 'Pitbull', 'gris', 5, 'macho', 'cojo', True, False),
    Perro('Luna', 'Golden', 'dorado', 3, 'hembra', 'sano', False, True)
]

gato = Gato('Michi', 'Siamés', 'blanco', 2, 'macho', 'sano')

peces = [
    Pez('Nemo', 'Clown', 'naranja', 1, 'macho', 'sano', 'salada'),
    Pez('Burbujas', 'Dorado', 'amarillo', 1, 'hembra', 'aleta herida', 'dulce'),
    Pez('Ray', 'Raya', 'gris', 2, 'macho', 'sano', 'salada'),
    Pez('Dory', 'Cirujano', 'azul', 1, 'hembra', 'sano', 'salada'),
    Pez('Flash', 'Betta', 'rojo', 1, 'macho', 'sano', 'dulce')
]

conejos = [
    Conejo('Pelusa', 'Mini Lop', 'blanco', 1, 'hembra', 'sano'),
    Conejo('Bruno', 'Holandés', 'negro', 2, 'macho', 'sano')
]

# Mostrar animales antes de la adopción
print('Animales antes de la adopción:\n')
for animal in perros + [gato] + conejos + peces:
    animal.mostrar_info()

# Simular adopciones
print('\nProceso de adopción:\n')
conejos[0].adoptar()
gato.adoptar()
adoptado = False
for perro in perros:
    if perro.adoptar():
        print(f'{perro.nombre} fue adoptado como perro apto para niños.')
        adoptado = True
        break
if not adoptado:
    print('No se encontró un perro apto para la adopción.')

# Mostrar animales después de la adopción
print('\nAnimales después de la adopción:\n')
for animal in perros + [gato] + conejos + peces:
    animal.mostrar_info()