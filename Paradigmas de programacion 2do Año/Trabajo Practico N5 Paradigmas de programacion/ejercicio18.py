import pygame
import sys # sys es útil para cerrar la aplicación de forma limpia

# --- 1. Inicialización ---
pygame.init()

# --- 2. Configuración de la Ventana ---
# Dimensiones [cite: 150]
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ventana de Juego con fondo Verde")

# Definición de colores (en RGB: Red, Green, Blue)
VERDE = (0, 255, 0) # [cite: 149]
# (La imagen de ejemplo [cite: 151] usa un verde lima, (50, 205, 50) 
# también funcionaría, pero (0, 255, 0) es el verde puro)

# --- 3. Bucle Principal (Game Loop) ---
running = True
while running:
    
    # --- 3.1. Manejo de Eventos ---
    for event in pygame.event.get():
        # Si el usuario hace clic en la 'X' de la ventana
        if event.type == pygame.QUIT:
            running = False

    # --- 3.2. Lógica (No hay en este ejercicio) ---
    # ...

    # --- 3.3. Dibujo en Pantalla ---
    # Rellenamos la pantalla con el color verde [cite: 149]
    screen.fill(VERDE)
    
    # Actualizamos la pantalla para mostrar los cambios
    pygame.display.flip()

# --- 4. Salir ---
pygame.quit()
sys.exit()