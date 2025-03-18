names = []
name_length = 1

while True:
    name = input(f'Ingrese el nombre numero {name_length} o zzz para salir: ')
    name_length+=1
    
    if name == 'zzz':
        print('Fin del ciclo')
        break
    names.append(name)

print(f'Nombres ingresados: {names}')