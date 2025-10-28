import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Personaje con Flechas")

NEGRO = (0, 0, 0)

# --- Cargar Recursos ---
try:
    personaje_img = pygame.image.load("personaje.png").convert_alpha() # 
except FileNotFoundError:
    print("Error: No se encontró el archivo 'personaje.png'")
    pygame.quit()
    sys.exit()

# Obtenemos el 'rect' (rectángulo) de la imagen para manejar su posición
personaje_rect = personaje_img.get_rect()
# Posición inicial (centrado)
personaje_rect.x = (WIDTH - personaje_rect.width) // 2
personaje_rect.y = (HEIGHT - personaje_rect.height) // 2

velocidad = 5

# --- Bucle Principal ---
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # --- 3.2. Lógica (Manejo de Teclas) ---
    # Obtenemos el estado de TODAS las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Movemos el personaje si la tecla está presionada 
    if keys[pygame.K_LEFT]:
        personaje_rect.x -= velocidad
    if keys[pygame.K_RIGHT]:
        personaje_rect.x += velocidad
    if keys[pygame.K_UP]:
        personaje_rect.y -= velocidad
    if keys[pygame.K_DOWN]:
        personaje_rect.y += velocidad
        
    # --- Verificación de Bordes  ---
    if personaje_rect.left < 0:
        personaje_rect.left = 0
    if personaje_rect.right > WIDTH:
        personaje_rect.right = WIDTH
    if personaje_rect.top < 0:
        personaje_rect.top = 0
    if personaje_rect.bottom > HEIGHT:
        personaje_rect.bottom = HEIGHT

    # --- 3.3. Dibujo ---
    screen.fill(NEGRO)
    screen.blit(personaje_img, personaje_rect)
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()