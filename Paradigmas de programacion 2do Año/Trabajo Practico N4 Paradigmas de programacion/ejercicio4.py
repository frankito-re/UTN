# Nombre alumno: Franco Genaro Reyes
def repetir_n_veces(n):
    def decorador(funcion_decorar):
        def funcion_decoradora():
            for _ in range(n):
                funcion_decorar()
        return funcion_decoradora
    return decorador

@repetir_n_veces(3)
def funcion_decorada():
    print('Me estoy ejecutando')

funcion_decorada()