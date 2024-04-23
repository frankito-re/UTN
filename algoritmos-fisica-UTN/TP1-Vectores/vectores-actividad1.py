# Implemente un programa para cambiar unidades de longitud (al menos 10).
def convertir_longitud(valor, unidad_origen, unidad_destino):
    conversiones = {
        'metros': {'milimetros': 1000, 'centimetros': 100, 'kilometros': 0.001, 'pies': 3.28084, 'pulgadas': 39.3701},
        'milimetros': {'metros': 0.001, 'centimetros': 0.1, 'kilometros': 1e-6, 'pies': 0.00328084, 'pulgadas': 0.0393701},
        'centimetros': {'metros': 0.01, 'milimetros': 10, 'kilometros': 1e-5, 'pies': 0.0328084, 'pulgadas': 0.393701},
        'kilometros': {'metros': 1000, 'milimetros': 1e+6, 'centimetros': 1e+5, 'pies': 3280.84, 'pulgadas': 39370.1},
        'pies': {'metros': 0.3048, 'milimetros': 304.8, 'centimetros': 30.48, 'kilometros': 0.0003048, 'pulgadas': 12},
        'pulgadas': {'metros': 0.0254, 'milimetros': 25.4, 'centimetros': 2.54, 'kilometros': 2.54e-5, 'pies': 0.0833333},
    }

    if unidad_origen in conversiones and unidad_destino in conversiones[unidad_origen]:
        factor_conversion = conversiones[unidad_origen][unidad_destino]
        valor_convertido = valor * factor_conversion
        return valor_convertido
    else:
        return None

valor_a_convertir = 5
unidad_origen = 'metros'
unidad_destino = 'pies'
resultado = convertir_longitud(valor_a_convertir, unidad_origen, unidad_destino)

if resultado is not None:
    print(f'{valor_a_convertir} {unidad_origen} es igual a {resultado} {unidad_destino}')
else:
    print('No se puede realizar la conversión. Verifique las unidades ingresadas.')