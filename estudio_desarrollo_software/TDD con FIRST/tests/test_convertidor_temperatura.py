# Desafío 2: Convertidor de Temperatura 🌡️
# Tenés que crear una función celsius_a_fahrenheit(celsius) que aplique estas dos reglas:
# Regla 1: Si recibe 0 grados Celsius, debe devolver exactamente 32.0 Fahrenheit.
# Regla 2: Si recibe 100 grados Celsius, debe devolver exactamente 212.0 Fahrenheit.
# (La fórmula matemática es: (celsius * 9/5) + 32).
from convertidor_temperatura import celsius_a_fahrenheit

def test_cero_celsius_es_32_fahrenheit():
    assert celsius_a_fahrenheit(0) == 32.0

def test_cien_celsius_es_212_fahrenheit():
    assert celsius_a_fahrenheit(100) == 212.0