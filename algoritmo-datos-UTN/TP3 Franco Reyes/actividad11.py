mark_array = [33, 11, 20, 2, 15, 1, 12, 11, 8, 14, 10]

lowest_mark = mark_array[0]
index_lowest_mark = 0

for mark in range(1, len(mark_array)):
    if mark_array[mark] < lowest_mark:
        lowest_mark = mark_array[mark]
        index_lowest_mark = mark
        
mark_array.pop(index_lowest_mark)

print('Nota más baja eliminada:', lowest_mark)

average = sum(mark_array) / len(mark_array)

print('Promedio de notas descontando la nota eliminada:', average)