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
pygame.display.set_caption("Invasores Espaciales (POO)")
reloj = pygame.time.Clock()
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# --- 2. Clases de Objetos del Juego ---

class Player(pygame.sprite.Sprite):
    """
    Clase para el jugador. Hereda de pygame.sprite.Sprite.
    Controla el movimiento, disparos, vidas e invulnerabilidad.
    """
    def __init__(self, assets):
        super().__init__()
        
        # Estado (Atributos)
        self.assets = assets
        self.image = assets['jugador']
        self.rect = self.image.get_rect(centerx = ANCHO // 2, bottom = ALTO - 20)
        self.velocidad = 5
        self.vidas = 3
        
        # Estado del escudo
        self.invulnerable = False
        self.tiempo_invulnerable_inicio = 0
        self.duracion_escudo = 5000 # 5 segundos
        self.escudo_efecto_rect = assets['escudo_efecto'].get_rect()
        
        # Estado de disparo
        self.puede_disparar = True
        
    def update(self):
        """ Actualiza la lógica del jugador en cada fotograma. """
        self.get_input()
        self.revisar_limites()
        self.revisar_invulnerabilidad()
        
        # Actualizar la posición del escudo visual
        self.escudo_efecto_rect.center = self.rect.center

    def get_input(self):
        """ Maneja el movimiento basado en las teclas presionadas. """
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidad

    def revisar_limites(self):
        """ Evita que el jugador salga de sus límites. """
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.top < ALTO // 2:
            self.rect.top = ALTO // 2
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
            
    def revisar_invulnerabilidad(self):
        """ Revisa si el escudo debe desactivarse. """
        if self.invulnerable:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_invulnerable_inicio > self.duracion_escudo:
                self.invulnerable = False

    def disparar(self):
        """ Crea y devuelve un objeto Bala si puede disparar. """
        if self.puede_disparar:
            self.puede_disparar = False # Solo una bala a la vez
            return Bala(self.assets['bala_jugador'], self.rect.midtop, -10)
        return None

    def recibir_daño(self):
        """ Resta una vida si no es invulnerable. """
        if not self.invulnerable:
            self.vidas -= 1
            if self.assets['sonido_hit_jugador']:
                self.assets['sonido_hit_jugador'].play()
            return True # Devuelve True si recibió daño
        return False # Devuelve False si estaba protegido

    def activar_escudo(self):
        """ Activa la invulnerabilidad. """
        self.invulnerable = True
        self.tiempo_invulnerable_inicio = pygame.time.get_ticks()
        if self.assets['sonido_powerup']:
            self.assets['sonido_powerup'].play()

    def dibujar_extra(self, pantalla):
        """ Dibuja elementos extra (como el escudo) sobre el jugador. """
        if self.invulnerable:
            pantalla.blit(self.assets['escudo_efecto'], self.escudo_efecto_rect)

class Alien(pygame.sprite.Sprite):
    """ Clase para un alien individual. """
    def __init__(self, assets, x, y):
        super().__init__()
        self.image = assets['alien']
        self.rect = self.image.get_rect(x=x, y=y)

class Bala(pygame.sprite.Sprite):
    """ Clase para las balas (del jugador y aliens). """
    def __init__(self, image, pos_midtop, velocidad):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(midtop = pos_midtop)
        self.velocidad = velocidad # Negativa para jugador (sube), Positiva para alien (baja)
        
    def update(self):
        """ Mueve la bala y la destruye si sale de pantalla. """
        self.rect.y += self.velocidad
        
        # Si se va por arriba (jugador) o por abajo (alien)
        if self.rect.bottom < 0 or self.rect.top > ALTO:
            self.kill() # self.kill() la elimina de todos los grupos

class PowerUp(pygame.sprite.Sprite):
    """ Clase para el power-up de escudo que cae. """
    def __init__(self, assets, pos_center):
        super().__init__()
        self.image = assets['escudo_powerup']
        self.rect = self.image.get_rect(center = pos_center)
        self.velocidad = 3
    
    def update(self):
        """ Mueve el power-up hacia abajo. """
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()

class Flota:
    """ Clase administradora para toda la flota de aliens. """
    def __init__(self, assets):
        self.assets = assets
        self.aliens_group = pygame.sprite.Group()
        self.velocidad_flota = 2
        self.direccion_flota = 1
        self.bajada_flota = 10
        self.timer_disparo_base = 800 # ms
        self.timer_disparo_actual = self.timer_disparo_base
        pygame.time.set_timer(ALIEN_DISPARA, self.timer_disparo_actual)

    def crear_flota(self, nivel_actual):
        """ Limpia la flota y crea una nueva basada en el nivel. """
        self.aliens_group.empty() # Limpia aliens anteriores
        
        filas_base = 3
        columnas_base = 5
        
        filas_aliens = min(filas_base + (nivel_actual - 1) // 2, 5) 
        columnas_aliens = min(columnas_base + nivel_actual - 1, 10) 
        
        espacio_horizontal = self.assets['alien'].get_width() + 20
        espacio_vertical = self.assets['alien'].get_height() + 10
        margen_superior = 50 + (nivel_actual - 1) * 10
        
        for fila in range(filas_aliens):
            for col in range(columnas_aliens):
                x = col * espacio_horizontal + 50 
                y = fila * espacio_vertical + margen_superior
                alien = Alien(self.assets, x, y)
                self.aliens_group.add(alien)
                
    def update(self):
        """ Mueve toda la flota como un bloque. """
        # Mover todos los aliens horizontalmente
        for alien in self.aliens_group.sprites():
            alien.rect.x += self.velocidad_flota * self.direccion_flota

        # Revisar si *algún* alien tocó un borde
        borde_tocado = False
        for alien in self.aliens_group.sprites():
            if alien.rect.right >= ANCHO or alien.rect.left <= 0:
                borde_tocado = True
                break

        # Si un borde se tocó, invertir dirección y bajar *toda* la flota
        if borde_tocado:
            self.direccion_flota *= -1
            for alien in self.aliens_group.sprites():
                alien.rect.y += self.bajada_flota
    
    def disparar(self):
        """ Elige un alien al azar y devuelve un objeto Bala. """
        if self.aliens_group.sprites():
            tirador = random.choice(self.aliens_group.sprites())
            return Bala(self.assets['bala_alien'], tirador.rect.midbottom, 7)
        return None
        
    def aumentar_dificultad(self, nivel_actual):
        """ Aumenta la velocidad de la flota y disparos. """
        self.velocidad_flota += 1
        self.timer_disparo_actual = max(200, self.timer_disparo_base - (nivel_actual * 50)) 
        pygame.time.set_timer(ALIEN_DISPARA, self.timer_disparo_actual)

class HUD:
    """ Clase para dibujar el HUD (vidas y puntaje) con Bitmap Font. """
    def __init__(self, assets):
        self.img_vida_icon = assets['vida_icon']
        self.numeral_images = assets['numerales']
        self.img_x = self.numeral_images['x']
        self.ancho_numeral = self.numeral_images['0'].get_width()
        
    def draw(self, pantalla, vidas, puntaje, nivel):
        """ Dibuja todos los elementos del HUD. """
        
        # --- Dibujar Vidas ---
        pantalla.blit(self.img_vida_icon, (10, 10))
        pantalla.blit(self.img_x, (10 + self.img_vida_icon.get_width() + 5, 10))
        
        try:
            vidas_str = str(vidas)
            img_vidas_num = self.numeral_images[vidas_str]
            pantalla.blit(img_vidas_num, (10 + self.img_vida_icon.get_width() + 5 + self.img_x.get_width() + 5, 10))
        except KeyError:
            # En caso de que las vidas sean > 9 (no tenemos esa imagen)
            pass 

        # --- Dibujar Puntaje ---
        score_str = f"{puntaje:06d}"
        start_x = ANCHO - 10 - (len(score_str) * self.ancho_numeral)
        
        current_x = start_x
        for char in score_str:
            img_num = self.numeral_images[char]
            pantalla.blit(img_num, (current_x, 10))
            current_x += self.ancho_numeral
        
        # --- Dibujar Nivel ---
        nivel_str = f"NIVEL {nivel}"
        # (Usamos la fuente por defecto para "NIVEL")
        texto_nivel = fuente_game_over.render(nivel_str, True, BLANCO) 
        PANTALLA.blit(texto_nivel, (ANCHO // 2 - texto_nivel.get_width() // 2, 10))

# --- 3. Eventos Personalizados ---
ALIEN_DISPARA = pygame.USEREVENT + 1

# --- 4. Fuentes Globales (para Game Over) ---
try:
    fuente_game_over = pygame.font.Font(None, 72)
    fuente_puntaje_final = pygame.font.Font(None, 60) 
except pygame.error as e:
    print(f"Error al cargar la fuente por defecto: {e}")
    pygame.quit()
    sys.exit()

# --- 5. Clase Principal del Juego ---

class Juego:
    """
    Clase principal que administra todos los objetos y el bucle del juego.
    """
    def __init__(self):
        self.pantalla = PANTALLA
        self.reloj = reloj
        self.assets = self.cargar_assets()
        self.nuevo_juego()
        self.running = True
        
    def cargar_assets(self):
        """ Carga todas las imágenes y sonidos en un diccionario. """
        assets = {}
        try:
            # Imágenes del Juego
            assets['fondo'] = pygame.transform.scale(pygame.image.load('assets/Backgrounds/blue.png').convert(), (ANCHO, ALTO))
            assets['jugador'] = pygame.transform.scale(pygame.image.load('assets/PNG/playerShip1_blue.png').convert_alpha(), (60, 60))
            assets['bala_jugador'] = pygame.transform.scale(pygame.image.load('assets/PNG/Lasers/laserBlue01.png').convert_alpha(), (10, 30))
            assets['alien'] = pygame.transform.scale(pygame.image.load('assets/PNG/Enemies/enemyBlack1.png').convert_alpha(), (40, 40))
            assets['bala_alien'] = pygame.transform.scale(pygame.image.load('assets/PNG/Lasers/laserRed12.png').convert_alpha(), (10, 30))
            assets['escudo_powerup'] = pygame.transform.scale(pygame.image.load('assets/PNG/Power-ups/powerupBlue_shield.png').convert_alpha(), (30, 30))
            assets['escudo_efecto'] = pygame.transform.scale(pygame.image.load('assets/PNG/Effects/shield3.png').convert_alpha(), (70, 70))

            # Assets del HUD
            ui_path = 'assets/PNG/UI/' 
            assets['vida_icon'] = pygame.image.load(f'{ui_path}playerLife1_blue.png').convert_alpha()
            
            numeral_images = {}
            for i in range(10):
                img_num = pygame.image.load(f'{ui_path}numeral{i}.png').convert_alpha()
                numeral_images[str(i)] = img_num
            img_x = pygame.image.load(f'{ui_path}numeralX.png').convert_alpha()
            numeral_images['x'] = img_x
            assets['numerales'] = numeral_images
            
            # Sonidos
            assets['sonido_explosion'] = pygame.mixer.Sound('assets/Bonus/sfx_zap.ogg')
            assets['sonido_hit_jugador'] = pygame.mixer.Sound('assets/Bonus/sfx_shieldDown.ogg')
            assets['sonido_powerup'] = pygame.mixer.Sound('assets/Bonus/sfx_shieldUp.ogg')

        except pygame.error as e:
            print(f"Error al cargar assets: {e}")
            pygame.quit()
            sys.exit()
            
        return assets

    def nuevo_juego(self):
        """ Configura o resetea el juego a su estado inicial. """
        # Estado del juego
        self.puntaje = 0
        self.nivel = 1
        self.game_over = False
        
        # Crear Grupos de Sprites
        # 'all_sprites' se usa para dibujar y actualizar la mayoría de los objetos
        self.all_sprites = pygame.sprite.Group()
        self.player_bala_group = pygame.sprite.Group()
        self.alien_balas_group = pygame.sprite.Group()
        self.powerups_group = pygame.sprite.Group()
        
        # Crear Objetos
        self.player = Player(self.assets)
        self.all_sprites.add(self.player) # Añadimos al jugador al grupo
        
        self.flota = Flota(self.assets)
        self.flota.crear_flota(self.nivel)
        
        self.hud = HUD(self.assets)
        
    def run(self):
        """ El bucle principal del juego. """
        while self.running:
            self.reloj.tick(60)
            self.manejar_eventos()
            self.actualizar_logica()
            self.dibujar_pantalla()

    def manejar_eventos(self):
        """ Maneja todos los inputs del usuario. """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
            
            if self.game_over: # Si perdimos, solo podemos cerrar
                continue
                
            # Eventos del juego (solo si no es game over)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    bala = self.player.disparar()
                    if bala:
                        self.all_sprites.add(bala)
                        self.player_bala_group.add(bala)
            
            if evento.type == ALIEN_DISPARA:
                bala_alien = self.flota.disparar()
                if bala_alien:
                    self.all_sprites.add(bala_alien)
                    self.alien_balas_group.add(bala_alien)

    def actualizar_logica(self):
        """ Actualiza toda la lógica y colisiones del juego. """
        if self.game_over:
            return # No actualizamos nada si perdimos

        self.all_sprites.update() 
        self.flota.update() # Actualiza el movimiento del enjambre

        # --- Revisar Colisiones ---
        
        # 1. Balas del Jugador vs Aliens
        aliens_impactados = pygame.sprite.groupcollide(
            self.player_bala_group, self.flota.aliens_group, True, True
        )
        for alien in aliens_impactados:
            self.puntaje += 100
            if self.assets['sonido_explosion']:
                self.assets['sonido_explosion'].play()
            
            # Chance de soltar power-up
            if random.randint(1, 5) == 1: # 20% de chance
                powerup = PowerUp(self.assets, alien.rect.center)
                self.all_sprites.add(powerup)
                self.powerups_group.add(powerup)
            
            # Como la bala se destruyó, permitimos disparar de nuevo
            self.player.puede_disparar = True 

        # 2. Balas Alien vs Jugador
        # spritecollide revisa UN sprite contra UN grupo. True = elimina la bala
        impactos_al_jugador = pygame.sprite.spritecollide(
            self.player, self.alien_balas_group, True
        )
        if impactos_al_jugador:
            if self.player.recibir_daño(): # Si el jugador no era invulnerable
                if self.player.vidas <= 0:
                    self.game_over = True

        # 3. Jugador vs Power-ups
        powerups_recogidos = pygame.sprite.spritecollide(
            self.player, self.powerups_group, True
        )
        if powerups_recogidos:
            self.player.activar_escudo()

        # 4. Revisar si la bala del jugador se fue (si falló)
        # Esto es por si la bala se va sin chocar con nada
        if not self.player_bala_group.sprites():
            self.player.puede_disparar = True
            
        # 5. Lógica de Siguiente Nivel
        if not self.flota.aliens_group.sprites(): # Si no quedan aliens
            self.siguiente_nivel()
            
    def dibujar_pantalla(self):
        """ Dibuja todo en la pantalla. """
        self.pantalla.blit(self.assets['fondo'], (0, 0))
        
        if not self.game_over:
            # La magia de los Grupos: .draw() dibuja CADA sprite del grupo
            self.all_sprites.draw(self.pantalla)
            self.flota.aliens_group.draw(self.pantalla) # Dibujamos los aliens
            
            # Dibujos "extra" que van encima
            self.player.dibujar_extra(self.pantalla) 
            
            # Dibujar HUD
            self.hud.draw(self.pantalla, self.player.vidas, self.puntaje, self.nivel)
        
        else:
            # --- Dibujo de Pantalla "Game Over" ---
            texto_go = fuente_game_over.render("GAME OVER", True, ROJO)
            texto_puntaje_titulo = fuente_puntaje_final.render("Puntaje Final:", True, BLANCO)
            self.pantalla.blit(texto_go, (ANCHO // 2 - texto_go.get_width() // 2, ALTO // 2 - 50))
            self.pantalla.blit(texto_puntaje_titulo, (ANCHO // 2 - texto_puntaje_titulo.get_width() // 2, ALTO // 2 + 30))
            
            # Dibujar puntaje final con Bitmap Font
            score_str = f"{self.puntaje:06d}"
            ancho_numeral = self.assets['numerales']['0'].get_width()
            start_x = ANCHO // 2 - (len(score_str) * ancho_numeral) // 2
            current_x = start_x
            for char in score_str:
                img_num = self.assets['numerales'][char]
                self.pantalla.blit(img_num, (current_x, ALTO // 2 + 80))
                current_x += ancho_numeral

        pygame.display.flip()
        
    def siguiente_nivel(self):
        """ Prepara el juego para el siguiente nivel. """
        self.nivel += 1
        self.flota.aumentar_dificultad(self.nivel)
        
        # Limpiar balas y power-ups restantes
        self.player_bala_group.empty()
        self.alien_balas_group.empty()
        self.powerups_group.empty()
        
        # Añadir todos los sprites existentes (menos el jugador) al grupo de 'todos'
        # para que .empty() los borre.
        self.all_sprites.add(self.player_bala_group.sprites())
        self.all_sprites.add(self.alien_balas_group.sprites())
        self.all_sprites.add(self.powerups_group.sprites())
        self.all_sprites.empty() # Vacía el grupo
        
        # Añadimos al jugador de nuevo (porque .empty() lo borró)
        self.all_sprites.add(self.player)
        
        # Centrar al jugador
        self.player.rect.centerx = ANCHO // 2
        self.player.rect.bottom = ALTO - 20
        
        # Crear la nueva flota (la flota se añade a sus propios grupos)
        self.flota.crear_flota(self.nivel)
        
        pygame.time.delay(1000)

# --- 6. Ejecución del Juego ---
if __name__ == "__main__":
    juego = Juego()
    juego.run()

pygame.quit()
sys.exit()