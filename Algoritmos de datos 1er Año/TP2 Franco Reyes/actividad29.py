notes_number = int(input('Ingresa en numero la cantidad de notas: '))

notes_list = []

for number in range(notes_number):
    note = float(input(f'Ingresa una nota {number+1}: '))
    notes_list.append(note)
    
print(notes_list)