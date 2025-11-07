import pygame
import sys
import random ### NUEVO ### Necesitaremos 'random'

# --- 1. Inicialización y Configuración ---
pygame.init()
pygame.font.init()
pygame.mixer.init() 

ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Invasores Espaciales - Gira")
reloj = pygame.time.Clock()
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0) ### NUEVO ###

fuente = pygame.font.Font(None, 36)
fuente_game_over = pygame.font.Font(None, 72) ### NUEVO ###

# --- 2. Cargar Assets ---
try:
    img_jugador_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/playerShip1_blue.png').convert_alpha()
    img_bala_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Lasers/laserBlue01.png').convert_alpha()
    img_alien_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Enemies/enemyBlack1.png').convert_alpha()
    ### NUEVO ###
    img_bala_alien_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Lasers/laserRed12.png').convert_alpha()
except pygame.error as e:
    print(f"Error al cargar imágenes: {e}")
    pygame.quit()
    sys.exit()

try:
    sonido_explosion = pygame.mixer.Sound('assets/kenney_space-shooter-redux/Bonus/sfx_zap.ogg')
    ### NUEVO ###
    sonido_hit_jugador = pygame.mixer.Sound('assets/kenney_space-shooter-redux/Bonus/sfx_shieldDown.ogg') # Sonido de cuando te pegan
except pygame.error:
    sonido_explosion = None
    sonido_hit_jugador = None

# Redimensionar imágenes
ancho_jugador = 60
alto_jugador = 60
img_jugador = pygame.transform.scale(img_jugador_original, (ancho_jugador, alto_jugador))
ancho_bala = 10
alto_bala = 30
img_bala = pygame.transform.scale(img_bala_original, (ancho_bala, alto_bala))
ancho_alien = 40
alto_alien = 40
img_alien = pygame.transform.scale(img_alien_original, (ancho_alien, alto_alien))
### NUEVO ###
ancho_bala_alien = 10
alto_bala_alien = 30
img_bala_alien = pygame.transform.scale(img_bala_alien_original, (ancho_bala_alien, alto_bala_alien))

# --- 3. Elementos del Juego ---
puntaje = 0
vidas = 3 ### NUEVO ###
game_over = False ### NUEVO ###

# Jugador
jugador_rect = img_jugador.get_rect(centerx = ANCHO // 2, bottom = ALTO - 20)
velocidad_jugador = 5

# Bala del Jugador
bala_rect = None 
velocidad_bala = 10

# Flota Alienígena
lista_aliens = []
# ... (código de creación de flota igual que antes) ...
filas_aliens = 5
columnas_aliens = 10
espacio_horizontal = ancho_alien + 20
espacio_vertical = alto_alien + 10
for fila in range(filas_aliens):
    for col in range(columnas_aliens):
        x = col * espacio_horizontal + 50
        y = fila * espacio_vertical + 50
        alien_rect = img_alien.get_rect(x=x, y=y)
        lista_aliens.append(alien_rect)

# Variables de Movimiento de Flota
velocidad_flota = 2
direccion_flota = 1
bajada_flota = 10

### NUEVO ### --- Lógica de Disparo Alien ---
balas_aliens = [] # Lista para guardar todas sus balas
velocidad_bala_alien = 7

### NUEVO ### --- Temporizador de Disparo Alien ---
# Creamos un evento personalizado de Pygame
ALIEN_DISPARA = pygame.USEREVENT + 1
# Le decimos a Pygame que "active" este evento cada 800 milisegundos
pygame.time.set_timer(ALIEN_DISPARA, 800) # 800ms = 0.8 segundos

# --- 4. Bucle Principal del Juego ---

while True:
    reloj.tick(60)

    # --- 5. Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not game_over: ### NUEVO ### Solo procesar juego si no perdimos
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if bala_rect is None:
                        bala_rect = img_bala.get_rect(midtop = jugador_rect.midtop)
            
            ### NUEVO ### Evento de Disparo Alien
            if evento.type == ALIEN_DISPARA:
                # Si todavía quedan aliens...
                if lista_aliens:
                    # Elegimos uno al azar para que dispare
                    tirador = random.choice(lista_aliens)
                    # Creamos la bala en su parte inferior central
                    nueva_bala = img_bala_alien.get_rect(midtop = tirador.midbottom)
                    balas_aliens.append(nueva_bala)
            
    # --- 6. Lógica del Juego ---
    
    if not game_over: ### NUEVO ### Solo mover si el juego está activo
        # Movimiento del Jugador (igual)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador_rect.x -= velocidad_jugador
        # ... (resto del movimiento y límites del jugador) ...
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jugador_rect.x += velocidad_jugador
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jugador_rect.y -= velocidad_jugador
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jugador_rect.y += velocidad_jugador
        if jugador_rect.left < 0:
            jugador_rect.left = 0
        if jugador_rect.right > ANCHO:
            jugador_rect.right = ANCHO
        if jugador_rect.top < ALTO // 2:
            jugador_rect.top = ALTO // 2
        if jugador_rect.bottom > ALTO:
            jugador_rect.bottom = ALTO

        # Lógica de Bala del Jugador y Colisiones (igual)
        if bala_rect is not None:
            bala_rect.y -= velocidad_bala
            alien_impactado = None
            for alien in lista_aliens:
                if bala_rect.colliderect(alien):
                    alien_impactado = alien
                    break
            if alien_impactado is not None:
                lista_aliens.remove(alien_impactado)
                bala_rect = None
                puntaje += 100
                if sonido_explosion:
                    sonido_explosion.play()
            elif bala_rect.bottom < 0:
                bala_rect = None 
                
        # Lógica de Movimiento de Flota (igual)
        borde_tocado = False
        for alien in lista_aliens:
            alien.x += velocidad_flota * direccion_flota
            if alien.right >= ANCHO or alien.left <= 0:
                borde_tocado = True
        if borde_tocado:
            direccion_flota *= -1
            for alien in lista_aliens:
                alien.y += bajada_flota
                
        ### NUEVO ### --- Lógica de Balas Alien ---
        # Usamos .copy() porque vamos a borrar elementos de la lista mientras la recorremos
        for bala in balas_aliens.copy():
            # Mover la bala hacia abajo
            bala.y += velocidad_bala_alien
            
            # Revisar colisión con el jugador
            if bala.colliderect(jugador_rect):
                vidas -= 1 # Restamos vida
                if sonido_hit_jugador:
                    sonido_hit_jugador.play()
                balas_aliens.remove(bala) # Eliminamos la bala
                
                if vidas <= 0:
                    game_over = True # ¡Perdimos!
            
            # Eliminar si sale de la pantalla
            elif bala.top > ALTO:
                balas_aliens.remove(bala)

    # --- 7. Dibujo en Pantalla ---
    
    PANTALLA.fill(NEGRO)
    
    if not game_over:
        # --- Dibujo del Juego ---
        PANTALLA.blit(img_jugador, jugador_rect)
        
        if bala_rect is not None:
            PANTALLA.blit(img_bala, bala_rect)
            
        for alien in lista_aliens:
            PANTALLA.blit(img_alien, alien)
            
        ### NUEVO ### Dibujar balas alien
        for bala in balas_aliens:
            PANTALLA.blit(img_bala_alien, bala)
            
        # Dibujar Puntaje (igual)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        PANTALLA.blit(texto_puntaje, (10, 10))
        
        ### NUEVO ### Dibujar Vidas
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
        PANTALLA.blit(texto_vidas, (ANCHO - 120, 10)) # Arriba a la derecha
        
    else:
        # --- Dibujo de Pantalla "Game Over" ---
        texto_go = fuente_game_over.render("GAME OVER", True, ROJO)
        texto_puntaje_final = fuente.render(f"Puntaje Final: {puntaje}", True, BLANCO)
        PANTALLA.blit(texto_go, (ANCHO // 2 - texto_go.get_width() // 2, ALTO // 2 - 50))
        PANTALLA.blit(texto_puntaje_final, (ANCHO // 2 - texto_puntaje_final.get_width() // 2, ALTO // 2 + 30))

    # --- 8. Actualización ---
    pygame.display.flip()