with open('/Users/d3ksur/own_proyects/UTN/algoritmo-datos-UTN/TP5 Franco Reyes/names.txt', 'w') as names:
    for name in range(5):
        name = input(f'Ingrese un nombre: ')
        names.write(f'{name} \n')