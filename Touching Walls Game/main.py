import pygame
import sys
import random

# --- 1. Inicialización y Configuración ---
pygame.init()
pygame.font.init()
pygame.mixer.init() 

ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Invasores Espaciales - Gira")
reloj = pygame.time.Clock()
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

try:
    fuente_game_over = pygame.font.Font(None, 72)
    fuente_puntaje_final = pygame.font.Font(None, 60) 
except pygame.error as e:
    print(f"Error al cargar la fuente por defecto: {e}")
    pygame.quit()
    sys.exit()


# --- 2. Cargar Assets ---
try:
    # --- Imágenes del Juego ---
    img_fondo_original = pygame.image.load('assets/kenney_space-shooter-redux/Backgrounds/blue.png').convert()
    img_jugador_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/playerShip1_blue.png').convert_alpha()
    img_bala_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Lasers/laserBlue01.png').convert_alpha()
    img_alien_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Enemies/enemyBlack1.png').convert_alpha()
    img_bala_alien_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Lasers/laserRed12.png').convert_alpha()
    img_escudo_powerup_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Power-ups/powerupBlue_shield.png').convert_alpha()
    img_escudo_efecto_original = pygame.image.load('assets/kenney_space-shooter-redux/PNG/Effects/shield3.png').convert_alpha()

    # --- Assets del HUD ---
    ui_path = 'assets/kenney_space-shooter-redux/PNG/UI/' 
    img_vida_icon = pygame.image.load(f'{ui_path}playerLife1_blue.png').convert_alpha()
    numeral_images = {}
    for i in range(10):
        img_num = pygame.image.load(f'{ui_path}numeral{i}.png').convert_alpha()
        numeral_images[str(i)] = img_num
    img_x = pygame.image.load(f'{ui_path}numeralX.png').convert_alpha()
    numeral_images['x'] = img_x

except pygame.error as e:
    print(f"Error al cargar imágenes (revisa las rutas, especialmente 'ui_path'): {e}")
    pygame.quit()
    sys.exit()

try:
    # --- Sonidos ---
    sonido_explosion = pygame.mixer.Sound('assets/kenney_space-shooter-redux/Bonus/sfx_zap.ogg')
    sonido_hit_jugador = pygame.mixer.Sound('assets/kenney_space-shooter-redux/Bonus/sfx_shieldDown.ogg')
    sonido_powerup = pygame.mixer.Sound('assets/kenney_space-shooter-redux/Bonus/sfx_shieldUp.ogg')
except pygame.error as e:
    print(f"Error al cargar sonidos: {e}")
    sonido_explosion = None
    sonido_hit_jugador = None
    sonido_powerup = None

# --- Redimensionar imágenes ---
img_fondo = pygame.transform.scale(img_fondo_original, (ANCHO, ALTO))
ancho_jugador = 60
alto_jugador = 60
img_jugador = pygame.transform.scale(img_jugador_original, (ancho_jugador, alto_jugador))
ancho_bala = 10
alto_bala = 30
img_bala = pygame.transform.scale(img_bala_original, (ancho_bala, alto_bala))
ancho_alien = 40
alto_alien = 40
img_alien = pygame.transform.scale(img_alien_original, (ancho_alien, alto_alien))
ancho_bala_alien = 10
alto_bala_alien = 30
img_bala_alien = pygame.transform.scale(img_bala_alien_original, (ancho_bala_alien, alto_bala_alien))
ancho_escudo_powerup = 30
alto_escudo_powerup = 30
img_escudo_powerup = pygame.transform.scale(img_escudo_powerup_original, (ancho_escudo_powerup, alto_escudo_powerup))
ancho_escudo_efecto = 70 
alto_escudo_efecto = 70
img_escudo_efecto = pygame.transform.scale(img_escudo_efecto_original, (ancho_escudo_efecto, alto_escudo_efecto))

# Ponemos la lógica de creación de flota en una función
# para poder llamarla en cada nivel
def crear_flota(nivel_actual):
    nueva_lista_aliens = []
    
    filas_base = 3
    columnas_base = 5
    
    filas_aliens = min(filas_base + (nivel_actual - 1) // 2, 5) 
    columnas_aliens = min(columnas_base + nivel_actual - 1, 10) 
    
    espacio_horizontal = ancho_alien + 20
    espacio_vertical = alto_alien + 10
    
    # Hacemos que la flota empiece un poco más abajo en cada nivel
    margen_superior = 50 + (nivel_actual - 1) * 10
    
    for fila in range(filas_aliens):
        for col in range(columnas_aliens):
            x = col * espacio_horizontal + 50 
            y = fila * espacio_vertical + margen_superior 
            
            # Creamos el Rect en esa posición
            alien_rect = img_alien.get_rect(x=x, y=y)
            
            # Añadimos el nuevo alien a nuestra lista
            nueva_lista_aliens.append(alien_rect)
    return nueva_lista_aliens

# --- 3. Elementos del Juego ---
puntaje = 0
vidas = 3
game_over = False
nivel = 1 

# Variables de Invulnerabilidad
jugador_invulnerable = False
tiempo_invulnerable_inicio = 0
DURACION_ESCUDO = 5000 

# Jugador
jugador_rect = img_jugador.get_rect(centerx = ANCHO // 2, bottom = ALTO - 20)
velocidad_jugador = 5
escudo_efecto_rect = img_escudo_efecto.get_rect()

# Bala del Jugador
bala_rect = None 
velocidad_bala = 10

# Flota Alienígena
lista_aliens = crear_flota(nivel)

# Variables de Movimiento de Flota
velocidad_flota = 2
direccion_flota = 1
bajada_flota = 10

# Lógica de Disparo Alien
balas_aliens = [] 
velocidad_bala_alien = 7
ALIEN_DISPARA = pygame.USEREVENT + 1
timer_disparo_actual = 800 
pygame.time.set_timer(ALIEN_DISPARA, timer_disparo_actual)

# Lista de Power-ups
escudos_powerup = [] 
velocidad_powerup = 3

# --- 4. Bucle Principal del Juego ---
while True:
    reloj.tick(60)
    ahora = pygame.time.get_ticks()

    # --- 5. Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not game_over:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if bala_rect is None:
                        bala_rect = img_bala.get_rect(midtop = jugador_rect.midtop)
            
            if evento.type == ALIEN_DISPARA:
                if lista_aliens:
                    tirador = random.choice(lista_aliens)
                    nueva_bala = img_bala_alien.get_rect(midtop = tirador.midbottom)
                    balas_aliens.append(nueva_bala)
            
    # --- 6. Lógica del Juego ---
    if not game_over:
        # Movimiento del Jugador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jugador_rect.x -= velocidad_jugador
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

        escudo_efecto_rect.center = jugador_rect.center

        # Lógica de Invulnerabilidad
        if jugador_invulnerable:
            if ahora - tiempo_invulnerable_inicio > DURACION_ESCUDO:
                jugador_invulnerable = False

        # Lógica de Bala del Jugador (sin cambios en colisión)
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
                if random.randint(1, 5) == 1:
                    nuevo_escudo = img_escudo_powerup.get_rect(center = alien_impactado.center)
                    escudos_powerup.append(nuevo_escudo)
            
            elif bala_rect is not None and bala_rect.bottom < 0:
                bala_rect = None
                
        # Lógica de Movimiento de Flota
        borde_tocado = False
        for alien in lista_aliens:
            alien.x += velocidad_flota * direccion_flota # Usa la variable global 'velocidad_flota'
            if alien.right >= ANCHO or alien.left <= 0:
                borde_tocado = True
        if borde_tocado:
            direccion_flota *= -1
            for alien in lista_aliens:
                alien.y += bajada_flota
                
        # Lógica de Balas Alien
        for bala in balas_aliens.copy():
            bala.y += velocidad_bala_alien
            if bala.colliderect(jugador_rect) and not jugador_invulnerable:
                vidas -= 1
                if sonido_hit_jugador:
                    sonido_hit_jugador.play()
                balas_aliens.remove(bala)
                if vidas <= 0:
                    game_over = True
                continue
            if bala.top > ALTO:
                balas_aliens.remove(bala)
                
        # Lógica de Power-ups de Escudo
        for escudo in escudos_powerup.copy():
            escudo.y += velocidad_powerup
            if jugador_rect.colliderect(escudo):
                jugador_invulnerable = True
                tiempo_invulnerable_inicio = ahora
                escudos_powerup.remove(escudo)
                if sonido_powerup:
                    sonido_powerup.play()
            elif escudo.top > ALTO:
                escudos_powerup.remove(escudo)
        
        # Si la lista de aliens está vacía, los matamos a todos
        if not lista_aliens:
            # 1. Aumentamos el nivel y la dificultad
            nivel += 1
            velocidad_flota += 1
            
            # Los aliens disparan más rápido (con un límite de 200ms)
            timer_disparo_actual = max(200, 800 - (nivel * 50)) 
            pygame.time.set_timer(ALIEN_DISPARA, timer_disparo_actual)
            
            # 2. Reseteamos la pantalla
            balas_aliens.clear()
            escudos_powerup.clear()
            
            # 3. Centramos al jugador
            jugador_rect.centerx = ANCHO // 2
            jugador_rect.bottom = ALTO - 20
            
            # 4. Creamos la nueva flota
            lista_aliens = crear_flota(nivel)
            
            pygame.time.delay(1000)


    # --- 7. Dibujo en Pantalla ---
    PANTALLA.blit(img_fondo, (0, 0))
    
    if not game_over:
        # --- Dibujo del Juego ---
        if bala_rect is not None:
            PANTALLA.blit(img_bala, bala_rect)
        for alien in lista_aliens:
            PANTALLA.blit(img_alien, alien)
        for bala in balas_aliens:
            PANTALLA.blit(img_bala_alien, bala)
        for escudo in escudos_powerup:
            PANTALLA.blit(img_escudo_powerup, escudo)
        PANTALLA.blit(img_jugador, jugador_rect)
        if jugador_invulnerable:
            PANTALLA.blit(img_escudo_efecto, escudo_efecto_rect)
            
        # --- Dibujo de HUD ---
        # Vidas
        PANTALLA.blit(img_vida_icon, (10, 10))
        img_x = numeral_images['x']
        PANTALLA.blit(img_x, (10 + img_vida_icon.get_width() + 5, 10))
        vidas_str = str(vidas)
        img_vidas_num = numeral_images[vidas_str]
        PANTALLA.blit(img_vidas_num, (10 + img_vida_icon.get_width() + 5 + img_x.get_width() + 5, 10))

        # Puntaje
        score_str = f"{puntaje:06d}"
        ancho_numeral = numeral_images['0'].get_width()
        start_x = ANCHO - 10 - (len(score_str) * ancho_numeral)
        current_x = start_x
        for char in score_str:
            img_num = numeral_images[char]
            PANTALLA.blit(img_num, (current_x, 10))
            current_x += ancho_numeral
        
        nivel_str = f"NIVEL {nivel}"
        texto_nivel = fuente_game_over.render(nivel_str, True, BLANCO) 
        PANTALLA.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, 10))

        
    else:
        texto_go = fuente_game_over.render("GAME OVER", True, ROJO)
        texto_puntaje_titulo = fuente_puntaje_final.render("Puntaje Final:", True, BLANCO)
        PANTALLA.blit(texto_go, (ANCHO // 2 - texto_go.get_width() // 2, ALTO // 2 - 50))
        PANTALLA.blit(texto_puntaje_titulo, (ANCHO // 2 - texto_puntaje_titulo.get_width() // 2, ALTO // 2 + 30))
        
        score_str = f"{puntaje:06d}"
        ancho_numeral = numeral_images['0'].get_width()
        start_x = ANCHO // 2 - (len(score_str) * ancho_numeral) // 2
        current_x = start_x
        for char in score_str:
            img_num = numeral_images[char]
            PANTALLA.blit(img_num, (current_x, ALTO // 2 + 80))
            current_x += ancho_numeral

    # --- 8. Actualización ---
    pygame.display.flip()