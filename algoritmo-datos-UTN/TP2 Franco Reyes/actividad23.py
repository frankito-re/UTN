student_marks = []

while len(student_marks) < 8:
    mark = int(input('Ingresa una nota: '))
    student_marks.append(mark)

average_marks = sum(student_marks) / len(student_marks)

print(round(average_marks, 1))