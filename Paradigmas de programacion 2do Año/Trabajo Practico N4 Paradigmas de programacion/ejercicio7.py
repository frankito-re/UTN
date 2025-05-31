# Nombre alumno: Franco Genaro Reyes
def validar_enteros(func):
    def wrapper(*args, **kwargs):
        for arg in args:
            if type(arg) != int:
                print('Error: todos los argumentos posicionales deben ser enteros.')
                return
        for valor in kwargs.values():
            if type(valor) != int:
                print('Error: todos los argumentos con nombre deben ser enteros.')
                return
        return func(*args, **kwargs)
    return wrapper

@validar_enteros
def sumar(a, b):
    print('La suma es:', a + b)

sumar(3, 4)
sumar(3, 'cuatro')