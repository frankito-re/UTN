import pygame
import sys

pygame.init()

# --- Configuración ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación por Sprites")
clock = pygame.time.Clock()
FONDO = (50, 50, 50)

# --- Configuración del Sprite ---
try:
    spritesheet = pygame.image.load("spritesheet.png").convert_alpha()
except FileNotFoundError:
    print("Error: Falta archivo 'spritesheet.png'")
    pygame.quit()
    sys.exit()

FRAME_WIDTH = 32 # Ancho de un fotograma
FRAME_HEIGHT = 32 # Alto de un fotograma
NUM_FRAMES = 8    # Cantidad de fotogramas en la hoja
ANIM_SPEED_MS = 100 # Milisegundos por fotograma (más rápido = más bajo)

# --- Cargamos los fotogramas ---
frames_derecha = []
frames_izquierda = []

for i in range(NUM_FRAMES):
    # 1. Recortamos el fotograma de la hoja
    rect_del_frame = pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
    frame = spritesheet.subsurface(rect_del_frame)
    
    # (Opcional: escalar la imagen si es muy chica)
    frame = pygame.transform.scale(frame, (FRAME_WIDTH * 2, FRAME_HEIGHT * 2))
    
    # 2. Guardamos el frame para la derecha
    frames_derecha.append(frame)
    
    # 3. Creamos un frame espejado y lo guardamos para la izquierda
    frame_flip = pygame.transform.flip(frame, True, False) # True=flip X, False=flip Y
    frames_izquierda.append(frame_flip)

# --- Estado del Jugador y Animación ---
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5
mirando_derecha = True
moviendose = False

frame_actual = 0
ultimo_update_anim = pygame.time.get_ticks()

# --- Bucle Principal ---
running = True
while running:
    
    ahora = pygame.time.get_ticks()

    # --- 1. Manejo de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 2. Lógica (Movimiento) ---
    keys = pygame.key.get_pressed()
    
    moviendose = False # Asumimos que no se mueve
    
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        mirando_derecha = False
        moviendose = True
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        mirando_derecha = True
        moviendose = True
        
    # (Aquí iría la lógica de límites de pantalla)

    # --- 2. Lógica (Animación) ---
    if moviendose:
        # Si está moviéndose, actualizamos el fotograma según el tiempo
        if ahora - ultimo_update_anim > ANIM_SPEED_MS:
            ultimo_update_anim = ahora
            frame_actual = (frame_actual + 1) % NUM_FRAMES # Avanza al sig. frame
    else:
        # Si está quieto, volvemos al fotograma 0 (idle)
        frame_actual = 0

    # --- 3. Dibujo (Render) ---
    screen.fill(FONDO)
    
    # Elegir la imagen correcta (frame y dirección)
    if mirando_derecha:
        imagen_actual = frames_derecha[frame_actual]
    else:
        imagen_actual = frames_izquierda[frame_actual]
        
    # Dibujar la imagen
    # (Ajustamos 'y' para que el 'centro' del personaje esté en player_y)
    pos_y_corregida = player_y - imagen_actual.get_height() // 2
    screen.blit(imagen_actual, (player_x, pos_y_corregida))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()