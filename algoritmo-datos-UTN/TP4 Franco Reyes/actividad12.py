def caracter_triangle(caracter: str, num: int):
    for i in range(num, 0, -1):
        print(caracter * i)

caracter_triangle('*', 6)