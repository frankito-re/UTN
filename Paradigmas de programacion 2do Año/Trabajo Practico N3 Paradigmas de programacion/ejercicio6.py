# Nombre alumno: Franco Genaro Reyes
class Celular:
    def __init__(self, modelo, precio):
        self.modelo = modelo
        self.precio = precio

lista_celulares = [Celular('Samsung Galaxy A54', 120000), 
                   Celular('Motorola G82', 100000), 
                   Celular('iPhone SE', 230000), 
                   Celular('Xiaomi Redmi Note 12', 110000), 
                   Celular('Nokia G60', 90000), 
                   Celular('Realme 11x', 85000)]

dinero_cliente = int(input('Ingrese la cantida de dinero que dispone para el celular: '))

lista_celulares_disponibles_cliente = [celular.modelo for celular in lista_celulares 
                                       if dinero_cliente >= celular.precio]

if len(lista_celulares_disponibles_cliente) == 0:
    print('Usted no dispone de suficiente dinero.')
else:
    print(f'Usted puede comprar los siguientes modelos: {lista_celulares_disponibles_cliente}.')