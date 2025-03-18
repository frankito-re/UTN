notas = [  ]
while len(notas) < 3:
    nota = int(input('Cual es la nota que sacaste? '))
    notas.append(nota)
promedio_final_porcentaje = (sum(notas) / len(notas)) * (100/10) # En esta parte podria poner 10 en vez de 100/10, pero prefiero que se entienda como calcular el porcentaje
print(f'Promedio final es: {promedio_final_porcentaje}')

if promedio_final_porcentaje >= 75:
    print('Usted promocionó la materia.')
elif 60 <= promedio_final_porcentaje < 75:
    print('Usted está regular en la materia.')
else:
    print('Usted no aprobo la materia')