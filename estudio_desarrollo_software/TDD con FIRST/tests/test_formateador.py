# El objetivo es crear una función formatear_nombre(nombre) que tome un nombre de usuario y aplique dos reglas 
# sencillas usando TDD y respetando los principios F.I.R.S.T.:
# Regla 1: Debe eliminar los espacios en blanco sobrantes al inicio y al final.
# Regla 2: Debe asegurar que la primera letra esté en mayúscula y las demás en minúscula.

from formateador import formatear_nombre


def test_eliminar_espacios_del_nombre():
    assert formatear_nombre(" Luis ") == "Luis"

def test_primera_letra_mayuscula():
    assert formatear_nombre("luis") == "Luis"

def test_letras_minusculas_menos_la_primera():
    assert formatear_nombre("LUIS") == "Luis"