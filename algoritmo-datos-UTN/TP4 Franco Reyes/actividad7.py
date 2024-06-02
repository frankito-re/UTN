def cuadrante(x: int, y: int):
    cuadrante = 'primer cuadrante'
    
    if x <= 0 and y >= 0:
        cuadrante = 'segundo cuadrante'
        
    if x <= 0 and y <= 0:
        cuadrante = 'tercer cuadreante'
        
    if x >= 0 and y <= 0:
        cuadrante = 'cuarto cuadrante'
        
    print(f'El cuadrante es: {cuadrante}') 
    
# Imprime cuarto cuadrante
cuadrante(2, -3)