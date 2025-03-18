def average(*args):
    num_sum = sum(args)
    num_average = num_sum / len(args)
    return num_average

# Ejemplo de uso
result = average(10, 20, 30, 40, 50)
print(f"El promedio de los números es {result}.")