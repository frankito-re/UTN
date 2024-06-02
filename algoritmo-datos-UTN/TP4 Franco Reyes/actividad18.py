def draw_hollow_rectangle_with_char(length, char):
    print(char * length)
    
    # Líneas del medio
    for _ in range(length - 2):
        print(char + " " * (length - 2) + char)
    
    print(char * length)

draw_hollow_rectangle_with_char(4, '#')
draw_hollow_rectangle_with_char(6, '*')