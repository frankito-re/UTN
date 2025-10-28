import pygame
import sys
import random

pygame.init()

# --- Configuración ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catching Stars")
clock = pygame.time.Clock()

# --- Colores y Fuente ---
FONDO_NOCHE = (10, 10, 40)
BLANCO = (255, 255, 255)
# Usamos una fuente por defecto de pygame
font = pygame.font.SysFont(None, 40) 

# --- Cargar Imágenes (Assets) ---
try:
    player_img = pygame.image.load("personaje.png").convert_alpha()
    star_img = pygame.image.load("estrella.png").convert_alpha()
except FileNotFoundError:
    print("Error: Faltan archivos 'personaje.png' o 'estrella.png'")
    pygame.quit()
    sys.exit()

# --- Jugador ---
player_rect = player_img.get_rect()
player_rect.midbottom = (WIDTH // 2, HEIGHT - 10) # Posición inicial abajo
player_speed = 8

# --- Estrellas ---
lista_estrellas = []
star_speed = 5
SPAWN_EVENT = pygame.USEREVENT + 1 # Evento personalizado para crear estrellas
pygame.time.set_timer(SPAWN_EVENT, 500) # Crear una estrella cada 500ms (0.5 seg)

# --- Puntuación ---
puntos = 0

# --- Bucle Principal ---
running = True
while running:
    
    # --- 1. Manejo de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Evento para crear una nueva estrella
        if event.type == SPAWN_EVENT:
            random_x = random.randint(0, WIDTH - star_img.get_width())
            star_rect = star_img.get_rect()
            star_rect.topleft = (random_x, -star_img.get_height()) # Aparece arriba
            lista_estrellas.append(star_rect)

    # --- 2. Lógica (Actualización) ---
    
    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
        
    # Mover estrellas y detectar colisiones
    # Iteramos sobre una copia de la lista (lista_estrellas[:])
    # para poder eliminar elementos de la original de forma segura.
    for star in lista_estrellas[:]:
        star.y += star_speed
        
        # Detección de colisión
        if player_rect.colliderect(star):
            puntos += 1 # Sumar punto
            lista_estrellas.remove(star) # Eliminar estrella
            
        # Eliminar estrellas que salen de pantalla
        elif star.top > HEIGHT:
            lista_estrellas.remove(star)

    # --- 3. Dibujo (Render) ---
    screen.fill(FONDO_NOCHE)
    
    # Dibujar jugador
    screen.blit(player_img, player_rect)
    
    # Dibujar todas las estrellas
    for star in lista_estrellas:
        screen.blit(star_img, star)
        
    # Dibujar puntuación
    score_text = font.render(f"Puntos: {puntos}", True, BLANCO)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()