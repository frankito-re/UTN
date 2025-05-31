# Nombre alumno: Franco Genaro Reyes
def decorador(funcion_decorar):
    def funcion_decoradora():
        print('La funcion se esta por ejecutar')
        funcion_decorar()
        print('La funcion ya se ejecuto')
    return funcion_decoradora

@decorador
def funcion_decorada():
    print('Me estoy ejecutando')

funcion_decorada()