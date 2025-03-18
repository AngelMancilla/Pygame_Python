import random
import pygame
from enemy import EnemyFast, ShooterEnemy, spawn_enemy
from player import Player
from settings import *
from powerups import PowerUp

# Inicialización de Pygame y mezcla de sonido
pygame.init()
pygame.mixer.init()

def load_image(path, size=None):
    """Carga una imagen desde el path y la escala si se especifica un tamaño."""
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_sound(path, volume=1.0):
    """Carga un sonido desde el path y ajusta el volumen."""
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

# Cargar música de fondo y efectos de sonido
pygame.mixer.music.load("assets/sounds/background_music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

shoot_sound = load_sound("assets/sounds/shoot.wav")
explosion_sound = load_sound("assets/sounds/explosion.wav")
enemy_explosion_sound = load_sound("assets/sounds/enemy_explosion.wav")
damage_sound = load_sound("assets/sounds/take_damage.wav")

# Configuración de la pantalla del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Python")
clock = pygame.time.Clock()

# Fuentes y texto
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 50)

# Fondo del juego
bg = pygame.image.load("assets/bg_space.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Diccionario de power-ups con sus imágenes
powerup_images = {
    "speed": load_image("assets/powerup_speed.png", (40, 40)),
    "shield": load_image("assets/powerup_shield.png", (40, 40)),
    "damage": load_image("assets/powerup_damage.png", (40, 40))
}

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# Variables del juego
score = 0
level = 1
points_to_level_up = 500
enemy_spawn_timer = 0
enemy_spawn_interval = 60
game_over = False

# Crear jugador
player = Player(WIDTH / 2, HEIGHT - 60, player_bullets, powerup_group, shoot_sound, damage_sound)
all_sprites.add(player)

def spawn_enemy(level, bullet_group):
    """Genera enemigos con dificultad basada en el nivel."""
    enemy_type = random.choice(["fast", "shooter"])

    if enemy_type == "fast":
        enemy = EnemyFast(random.randint(50, WIDTH - 50), random.randint(-100, -40))
    else:
        enemy = ShooterEnemy(random.randint(50, WIDTH - 50), random.randint(-100, -40), bullet_group)

    enemy_group.add(enemy)

def spawn_powerup(x, y):
    """Genera power-ups aleatorios con mayor probabilidad en niveles altos."""
    if random.random() < 0.3 + (level * 0.05):
        powerup_type = random.choice(["speed", "shield", "damage"])
        powerup = PowerUp(x, y, powerup_type)
        powerup_group.add(powerup)

def draw_ui():
    """Dibuja la interfaz de usuario con puntuación y barra de vida."""
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))

    screen.blit(score_text, (WIDTH - 180, 20))
    screen.blit(level_text, (WIDTH - 180, 50))

    # Barra de vida del jugador
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, 150, 20))  # Fondo rojo (vida máxima)
    pygame.draw.rect(screen, (0, 255, 0), (20, 20, max(0, 150 * (player.health / 100)), 20))  # Barra verde (vida actual)

def draw_powerups():
    """Dibuja los power-ups activos del jugador."""
    x = 20
    y = HEIGHT - 60  # Esquina inferior izquierda

    for powerup, active in player.powerups.items():
        if active:  # Si el power-up está activo, dibujarlo
            screen.blit(powerup_images[powerup], (x, y))
            x += 50  # Espacio entre iconos de power-ups

def show_game_over():
    """Muestra la pantalla de 'Game Over' al final del juego."""
    screen.fill((0, 0, 0))  # Fondo negro
    text = large_font.render(f'GAME OVER - Score: {score}', True, (255, 0, 0))
    level_text = large_font.render(f'Level Reached: {level}', True, (255, 255, 255))

    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2))

    retry_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

def handle_events():
    """Maneja los eventos del juego, como salir o reiniciar."""
    global running, game_over, waiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar el juego
                restart_game()
            elif event.key == pygame.K_q:  # Salir del juego
                running = False

def restart_game():
    """Reinicia el juego cuando el jugador muere y presiona 'R'."""
    global score, level, game_over
    player = Player(WIDTH / 2, HEIGHT - 60, player_bullets, powerup_group, shoot_sound, damage_sound)
    all_sprites.empty()
    enemy_group.empty()
    powerup_group.empty()
    all_sprites.add(player)
    score = 0
    level = 1
    game_over = False

# Bucle principal del juego
running = True
while running:
    screen.blit(bg, (0, 0))  # Dibuja el fondo del juego

    handle_events()  # Maneja los eventos

    if game_over:
        show_game_over()  # Muestra la pantalla de 'Game Over'
        pygame.display.flip()
        continue  # No se ejecuta más código si el juego terminó

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    player.move(keys)
    if keys[pygame.K_SPACE]:
        player.shoot()

    # Actualizar todos los sprites
    all_sprites.update()
    enemy_group.update()
    player_bullets.update()
    enemy_bullets.update()
    powerup_group.update()

    # Detección de colisiones con enemigos
    if pygame.sprite.spritecollide(player, enemy_group, True):
        player.take_damage(20)  # El jugador recibe daño al colisionar con un enemigo
    if pygame.sprite.spritecollide(player, enemy_bullets, True):
        player.take_damage(10)  # El jugador recibe daño al ser alcanzado por balas enemigas

    # Spawneo de enemigos cada cierto intervalo
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= enemy_spawn_interval:
        for _ in range(level + 1):  # Genera más enemigos conforme al nivel
            spawn_enemy(level, enemy_bullets)
        enemy_spawn_timer = 0

    # Detección de colisiones de balas del jugador con enemigos
    for bullet in player_bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
        if hit_enemies:
            bullet.kill()  # La bala se destruye al impactar
            enemy_explosion_sound.play()  # Sonido de explosión
            score += 100  # Se suman puntos por eliminar enemigos
            for enemy in hit_enemies:
                spawn_powerup(enemy.rect.centerx, enemy.rect.centery)  # Posible spawn de power-up

    # Subir de nivel y ajustar la dificultad
    if score >= level * points_to_level_up:
        level += 1
        enemy_spawn_interval = max(30, enemy_spawn_interval - 5)  # Los enemigos aparecen más rápido

    # Comprobar si la salud del jugador llegó a 0
    if player.health <= 0:
        explosion_sound.play()  # Sonido de explosión al morir
        game_over = True  # El juego termina

    # Dibujar todos los sprites y la UI
    all_sprites.draw(screen)
    enemy_group.draw(screen)
    player_bullets.draw(screen)
    enemy_bullets.draw(screen)
    powerup_group.draw(screen)

    draw_ui()  # Dibuja la puntuación y la vida
    draw_powerups()  # Dibuja los power-ups activos

    pygame.display.flip()  # Actualiza la pantalla
    clock.tick(FPS)  # Controla los frames por segundo

# Finalizar Pygame
pygame.quit()



