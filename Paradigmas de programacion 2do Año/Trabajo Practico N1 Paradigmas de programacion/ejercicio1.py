nota = int(input("Que saco en el ultimo examen? "))

if 6 <= nota <= 10:
    print('Usted aprobo el examen')
    
elif 0 < nota < 10:
    print('La nota no es posible')
    
else:
    print('Usted no aprobo')