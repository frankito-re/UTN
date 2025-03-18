import random

def average_throws(throws_num):
    throws = [random.randint(1, 6) for _ in range(throws_num)]
    average = sum(throws) / throws_num
    return average

average = average_throws(20)
print(f"El promedio de las 20 tiradas es: {average}")
