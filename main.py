import random
import pygame
from enemy import EnemyFast, ShooterEnemy
from player import *
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Python")
clock = pygame.time.Clock()

# Fuente para la puntuación
font = pygame.font.Font(None, 36)

# Fondo del juego
bg = pygame.image.load("assets/bg_space.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))  # Ajusta el fondo a la nueva resolución

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Variables de juego
score = 0  # Puntuación
level = 1  # Nivel inicial
points_to_level_up = 500  # Puntos necesarios para subir de nivel
enemy_spawn_timer = 0  # Temporizador para la aparición de enemigos
enemy_spawn_interval = 60  # Cada 60 frames (~1 segundo)
game_over = False
paused = False

# Crear el jugador
player = Player(WIDTH / 2, HEIGHT - 60, player_bullets)
all_sprites.add(player)


def spawn_enemy():
    """Genera enemigos continuamente con dificultad según el nivel."""
    enemy_type = random.choice(["fast", "shooter"])

    if enemy_type == "fast":
        enemy = EnemyFast(random.randint(50, WIDTH - 50), random.randint(-100, -40))
    else:
        enemy = ShooterEnemy(random.randint(50, WIDTH - 50), random.randint(-100, -40), enemy_bullets)

    enemy_group.add(enemy)


def show_game_over(screen, score, level):
    """Mostrar la puntuación y nivel al morir."""
    font = pygame.font.SysFont('Arial', 48)
    text = font.render(f'Game Over - Score: {score} Level: {level}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # Instrucciones para continuar o salir
    continue_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    continue_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(continue_text, continue_rect)

    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        paused = True
        show_game_over(screen, score, level)  # Mostrar puntuación y nivel
        pygame.time.wait(2000)  # Espera 2 segundos antes de mostrar las opciones
        # Manejar eventos para reiniciar o salir
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar juego con "R"
                    player = Player(WIDTH / 2, HEIGHT - 60, player_bullets)
                    all_sprites.add(player)
                    enemy_group.empty()
                    score = 0
                    level = 1
                    game_over = False
                    paused = False
                elif event.key == pygame.K_q:  # Salir con "Q"
                    pygame.quit()
                    quit()

    # Detectar teclas
    keys = pygame.key.get_pressed()

    if not paused:  # Si el juego no está pausado
        player.move(keys)
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Actualizar objetos
        all_sprites.update()
        enemy_group.update()
        player_bullets.update()
        enemy_bullets.update()

        # Spawneo de enemigos basado en tiempo y nivel
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            # Reducimos la cantidad de enemigos por oleada
            for _ in range(level + 1):  # Menos enemigos por oleada
                spawn_enemy()
            enemy_spawn_timer = 0  # Reiniciar el temporizador

        # Detectar colisiones de balas con enemigos
        for bullet in player_bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
            if hit_enemies:
                bullet.kill()
                score += 100

        # Subir de nivel si la puntuación alcanza el umbral
        if score >= level * points_to_level_up and level < 3:
            level += 1
            enemy_spawn_interval = max(30, enemy_spawn_interval - 10)  # Aumenta la frecuencia de aparición

        # Comprobar si la salud del jugador llega a 0
        if player.health <= 0:
            game_over = True
            paused = True

        # Dibujar en pantalla
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        enemy_group.draw(screen)
        player_bullets.draw(screen)
        enemy_bullets.draw(screen)

        # Mostrar la puntuación y nivel
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 150, 20))
        screen.blit(level_text, (WIDTH - 150, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

