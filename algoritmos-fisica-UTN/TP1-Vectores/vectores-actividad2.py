# Implemente un programa para cambiar unidades de tiempo (al menos 10)
def convertir_tiempo(valor, unidad_origen, unidad_destino):
    conversiones = {
        'segundos': {'milisegundos': 1000, 'minutos': 1/60, 'horas': 1/3600, 'dias': 1/86400, 'semanas': 1/604800, 'años': 1/31536000},
        'milisegundos': {'segundos': 0.001, 'minutos': 1/60000, 'horas': 1/3600000, 'dias': 1/86400000, 'semanas': 1/604800000, 'años': 1/31536000000},
        'minutos': {'segundos': 60, 'milisegundos': 60000, 'horas': 1/60, 'dias': 1/1440, 'semanas': 1/10080, 'años': 1/525600},
        'horas': {'segundos': 3600, 'milisegundos': 3600000, 'minutos': 60, 'dias': 1/24, 'semanas': 1/168, 'años': 1/8760},
        'dias': {'segundos': 86400, 'milisegundos': 86400000, 'minutos': 1440, 'horas': 24, 'semanas': 1/7, 'años': 1/365},
        'semanas': {'segundos': 604800, 'milisegundos': 604800000, 'minutos': 10080, 'horas': 168, 'dias': 7, 'años': 1/52.143},
        'años': {'segundos': 31536000, 'milisegundos': 31536000000, 'minutos': 525600, 'horas': 8760, 'dias': 365, 'semanas': 52.143},
    }

    if unidad_origen in conversiones and unidad_destino in conversiones[unidad_origen]:
        factor_conversion = conversiones[unidad_origen][unidad_destino]
        valor_convertido = valor * factor_conversion
        return valor_convertido
    else:
        return None

valor_a_convertir = 3
unidad_origen = 'dias'
unidad_destino = 'horas'
resultado = convertir_tiempo(valor_a_convertir, unidad_origen, unidad_destino)

if resultado is not None:
    print(f'{valor_a_convertir} {unidad_origen} es igual a {resultado} {unidad_destino}')
else:
    print('No se puede realizar la conversión. Verifique las unidades ingresadas.')
