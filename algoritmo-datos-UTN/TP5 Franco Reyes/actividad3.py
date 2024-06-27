def potencia(base:int, power:int):
    if power == 0:
        return 1
    return base * potencia(base, power - 1)


print(potencia(5, 6))