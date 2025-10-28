import pygame
import sys

pygame.init()

# --- Configuración de la Ventana ---
WIDTH, HEIGHT = 1200, 800 # [cite: 153]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mi Juego con Imagen PNG") # [cite: 153]

# Colores
AZUL_OSCURO = (0, 0, 40) # Un color de fondo diferente [cite: 155]

# --- Cargar Recursos (Assets) ---
try:
    # Carga una imagen. Asegúrate de tener una imagen PNG en la carpeta 
    mi_personaje = pygame.image.load("mi_imagen.png").convert_alpha() # [cite: 155]
    # .convert_alpha() optimiza la imagen para dibujarla con transparencias
except FileNotFoundError:
    print("Error: No se encontró el archivo 'mi_imagen.png'")
    pygame.quit()
    sys.exit()

# --- Bucle Principal ---
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Dibujo ---
    # 1. Rellenar el fondo
    screen.fill(AZUL_OSCURO)
    
    # 2. "Blit" (pegar) la imagen en la pantalla en las coordenadas (x, y)
    # (0, 0) es la esquina superior izquierda
    screen.blit(mi_personaje, (500, 300)) # La dibujamos cerca del centro

    # 3. Actualizar
    pygame.display.flip()

pygame.quit()
sys.exit()