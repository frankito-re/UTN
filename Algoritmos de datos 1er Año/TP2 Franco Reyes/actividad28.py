import random
brand_names = input('Ingresa tus marcas favoritas: ')

names_list = brand_names.split()

print(random.choice(names_list))