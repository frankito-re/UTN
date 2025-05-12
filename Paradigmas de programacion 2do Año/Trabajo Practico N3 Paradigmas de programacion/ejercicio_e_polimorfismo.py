# Nombre alumno: Franco Genaro Reyes
class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __lt__(self, otra):  # menor que
        return self.edad < otra.edad

    def __le__(self, otra):  # menor o igual
        return self.edad <= otra.edad

    def __gt__(self, otra):  # mayor que
        return self.edad > otra.edad

    def __ge__(self, otra):  # mayor o igual
        return self.edad >= otra.edad

    def __str__(self):
        return f'{self.nombre} ({self.edad} años)'


def verificar_acceso(p1, p2):
    if abs(p1.edad - p2.edad) >= 10:
        tutor = p1 if p1 > p2 else p2
        invitado = p2 if tutor == p1 else p1
        print(f'\n Pueden ingresar. {tutor.nombre} será el tutor de {invitado.nombre}.')
    else:
        print('\n No pueden ingresar. La diferencia de edad no es suficiente para definir un tutor.')


# Programa principal
print('🎉 Fiesta: ingreso de a pares (uno debe ser tutor)')
for i in range(1, 4):  # 3 pares como ejemplo
    print(f'\nPar #{i}')
    nombre1 = input('Nombre de la primera persona: ')
    edad1 = int(input('Edad: '))
    nombre2 = input('Nombre de la segunda persona: ')
    edad2 = int(input('Edad: '))

    p1 = Persona(nombre1, edad1)
    p2 = Persona(nombre2, edad2)

    verificar_acceso(p1, p2)