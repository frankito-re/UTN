# Nombre alumno: Franco Genaro Reyes
def acceso_por_rol(rol_requerido):
    def decorador(func):
        def wrapper(*args, **kwargs):
            if rol_requerido == 'admin':
                return func(*args, **kwargs)
            else:
                print('Acceso denegado. Rol insuficiente.')
        return wrapper
    return decorador

@acceso_por_rol('admin')
def panel_de_control():
    print('Accediste al panel de control.')

@acceso_por_rol('usuario')
def ver_estadisticas():
    print('Mostrando estadísticas.')

panel_de_control()
ver_estadisticas()