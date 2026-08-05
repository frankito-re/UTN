# Tenés que crear una función calcular_descuento(monto) que aplique estas dos reglas:
# Regla 1: Si el monto de compra es menor a 100, el descuento es 0.
# Regla 2: Si el monto es 100 o más, el descuento es del 10% (por ejemplo, para 150 debe devolver 15).
from calcular_descuento import calcular_descuento

def test_monto_es_100_descuesto_es_0():
    assert calcular_descuento(99) == 0

def test_monto_mayor_o_igual_a_100_descueto_10_porciento():
    assert calcular_descuento(100) == 10