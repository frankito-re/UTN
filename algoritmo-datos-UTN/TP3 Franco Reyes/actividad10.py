import random

seats = [random.choice([True, False]) for _ in range(0, 30)]

occupied_seats = seats.count(True)
free_seats = seats.count(False)

print(f'La cantidad de acientos ocupados es: {occupied_seats} y de acientos desocupados es: {free_seats}')
