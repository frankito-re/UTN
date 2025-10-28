import pygame
import sys
import random

pygame.init()

# --- Configuración ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evita los Enemigos")
clock = pygame.time.Clock()

# --- Colores y Fuente ---
FONDO_DIA = (135, 206, 235) # Celeste
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
font = pygame.font.SysFont(None, 40)
font_game_over = pygame.font.SysFont(None, 80)

# --- Cargar Imágenes (Assets) ---
try:
    player_img = pygame.image.load("personaje.png").convert_alpha()
    enemy_img = pygame.image.load("enemigo.png").convert_alpha()
except FileNotFoundError:
    print("Error: Faltan archivos 'personaje.png' o 'enemigo.png'")
    pygame.quit()
    sys.exit()

# --- Jugador ---
player_rect = player_img.get_rect()
player_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
player_speed = 8

# --- Enemigos ---
lista_enemigos = []
enemy_speed_inicial = 4
enemy_speed = enemy_speed_inicial
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1000) # Un enemigo por segundo

# --- Estado del Juego ---
score = 0
game_over = False # Estado para terminar el juego

# --- Bucle Principal ---
running = True
while running:
    
    # --- 1. Manejo de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == SPAWN_EVENT:
                random_x = random.randint(0, WIDTH - enemy_img.get_width())
                enemy_rect = enemy_img.get_rect()
                enemy_rect.topleft = (random_x, -enemy_img.get_height())
                lista_enemigos.append(enemy_rect)

    # --- 2. Lógica (Solo si el juego no ha terminado) ---
    if not game_over:
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
            
        # Aumentar dificultad 
        # Aumenta la velocidad un poco cada frame
        enemy_speed += 0.005 

        # Mover enemigos y detectar colisiones
        for enemy in lista_enemigos[:]:
            enemy.y += int(enemy_speed) # Usamos int() porque la pos es entera
            
            # Colisión = Fin del juego 
            if player_rect.colliderect(enemy):
                game_over = True
                
            # Enemigo esquivado
            elif enemy.top > HEIGHT:
                score += 1 # Sumamos puntos por esquivar
                lista_enemigos.remove(enemy)

    # --- 3. Dibujo (Render) ---
    screen.fill(FONDO_DIA)
    
    # Dibujar jugador y enemigos
    screen.blit(player_img, player_rect)
    for enemy in lista_enemigos:
        screen.blit(enemy_img, enemy)
        
    # Dibujar puntuación
    score_text = font.render(f"Esquivados: {score}", True, NEGRO)
    screen.blit(score_text, (10, 10))
    
    # Pantalla de Game Over
    if game_over:
        game_over_text = font_game_over.render("¡JUEGO TERMINADO!", True, ROJO)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()