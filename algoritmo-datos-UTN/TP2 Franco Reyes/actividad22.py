names_quantity = int(input('Ingrese la cantidad de nombres que quiere ingresar: '))

names = []
surnames = []

for full_name in range(names_quantity):
    full_name = input('Ingresa tu nombre completo: ').split()
    names.append(full_name[0])
    surnames.append(full_name[1])

print(f'Los nombres son: {names}')
print(f'Los apellidos son: {surnames}')