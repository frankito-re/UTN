import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cuadrado Rebotando")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255) # [cite: 156]

# --- Estado del Cuadrado ---
cuadrado_ancho = 50
cuadrado_alto = 50
cuadrado_x = 100 # Posición X inicial
cuadrado_y = 275 # Posición Y (fija)
velocidad_x = 5 # Píxeles que se mueve por fotograma

# 'Clock' nos ayuda a controlar la velocidad del juego (FPS)
clock = pygame.time.Clock()

# --- Bucle Principal ---
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 3.2. Actualizar la Lógica ---
    # Movemos el cuadrado [cite: 157]
    cuadrado_x += velocidad_x
    
    # Lógica de Rebote [cite: 157]
    # Si el borde izquierdo del cuadrado (cuadrado_x) toca el borde izquierdo (0)
    # O si el borde derecho (cuadrado_x + ancho) toca el borde derecho (WIDTH)
    if cuadrado_x <= 0 or (cuadrado_x + cuadrado_ancho) >= WIDTH:
        # Invertimos la velocidad para que rebote
        velocidad_x = velocidad_x * -1

    # --- 3.3. Dibujo ---
    screen.fill(NEGRO)
    
    # Creamos un objeto Rect para el cuadrado
    rect_azul = pygame.Rect(cuadrado_x, cuadrado_y, cuadrado_ancho, cuadrado_alto)
    pygame.draw.rect(screen, AZUL, rect_azul) # [cite: 156]

    pygame.display.flip()
    
    # Controlamos que el bucle se ejecute 60 veces por segundo (60 FPS)
    clock.tick(60)

pygame.quit()
sys.exit()