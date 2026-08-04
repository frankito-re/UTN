# test_validador.py
from validador import validar_contrasenia

def test_debe_fallar_si_tiene_menos_de_8_caracteres():
    # Una contraseña corta debería dar False
    assert validar_contrasenia("abc") == False

def test_falla_si_no_hay_numeros():
    assert validar_contrasenia("sdaskjasgdahjsg") == False