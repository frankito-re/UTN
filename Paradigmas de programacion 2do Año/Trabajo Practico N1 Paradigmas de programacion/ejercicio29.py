# Obtener un cuento corto, desde un archivo de texto llamado cuento.txt (Busque algun
# parrafo o cuento corto clasico y guardelo en un archivo de texto con dicho nombre).
# Realizar el siguiente analisis y mostrar en pantalla un informe de:
# a) Cuantas palabras contiene en total.
# b) Cuantas frases contiene en total. (¿Como debera distinguir una frase de otra?)
# c) Cuantos nombres propios o nombres de lugares hay en total.
# d) El total de vocales que contiene ese cuento.
# e) Cuantas palabras de longitud par existen.
# f ) Cuantas palabras de longitud impar contiene.
import string

file = open("/Users/d3ksur/Proyectos Mios/UTN/Paradigmas de programacion 2do Año/Trabajo Practico N1 Paradigmas de programacion/cuento.txt", "r")
cuento = file.read()

splited_words = cuento.split()

# Cuantas palabras contiene en total
print(f'La cantidad de palabras que hay son: {len(splited_words)}')

# Cuantas frases contiene en total. (¿Como debera distinguir una frase de otra?)
phrases_counter = 0
for l in cuento:
    if l == '.':
        phrases_counter += 1
print(f'La cantidad de frases que hay es: {phrases_counter}')

# Cuantos nombres propios o nombres de lugares hay en total.
name_city_counter = 0
for l in cuento:
    if l.isupper():
        name_city_counter+=1
    elif l == '.' and name_city_counter > 0:
        name_city_counter-=1
print(f'La cantidad de nombres propios o nombres de lugares que hay es: {name_city_counter}')

# El total de vocales que contiene ese cuento.
vowels = ['a', 'e', 'i', 'o', 'u']

vowels_counter = 0
for l in cuento:
    if l in vowels:
        vowels_counter += 1
print(f'La cantidad de vocales que hay es: {vowels_counter}')

# Cuantas palabras de longitud par existen.
pair_lenth_words_counter = 0
odd_lenth_words_counter = 0

for w in splited_words:
    clean_word = w.strip(string.punctuation)
    if len(clean_word) % 2 == 0:
        pair_lenth_words_counter+=1
    else:
        odd_lenth_words_counter+=1
print(f'La cantidad de palabras de longitud par que hay son: {pair_lenth_words_counter}')

#Cuantas palabras de longitud impar contiene.
print(f'La cantidad de palabras de longitud impar que hay son: {odd_lenth_words_counter}')          
