import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group):
        super().__init__()

        self.original_image = pygame.image.load('assets/player_ship.png').convert_alpha()  # Cargar la imagen original
        self.image = self.original_image
        self.image.set_colorkey((0, 0, 0))  # Eliminar el color de fondo (si es necesario)

        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 5
        self.health = 100
        self.level = 1
        self.score = 0  # Puntuación

        self.bullet_group = bullet_group
        self.shoot_cooldown = 0

        self.powerups = {
            "speed": False,
            "shield": False,
            "damage": False,
        }
        self.powerup_timers = {}

        self.explosion_frames = self.load_explosion_frames()  # Cargar frames de explosión
        self.explosion_frame_index = 0
        self.is_exploding = False

    def load_explosion_frames(self):
        # Cargar las imágenes para la animación de explosión
        frames = []
        for i in range(1, 6):  # Supón que tienes 5 imágenes de explosión
            frames.append(pygame.image.load(f'assets/FB00_nyknck/FB00_nyknck/FB00{i}.png').convert_alpha())
        return frames

    def move(self, keys):
        if self.is_exploding:  # No permite mover al jugador si está explotando
            return

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def update_image(self):
        # No hacemos ninguna rotación, ya que la imagen siempre debe ir hacia arriba
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        """Dispara balas si el cooldown lo permite"""
        if self.shoot_cooldown == 0:
            bullet = PlayerBullet(self.rect.centerx, self.rect.top)
            self.bullet_group.add(bullet)
            self.shoot_cooldown = 15

    def take_damage(self, amount):
        """Reduce la vida del jugador"""
        if not self.powerups["shield"]:
            self.health -= amount
        if self.health <= 0:
            self.explode()

    def explode(self):
        """Genera una explosión cuando el jugador muere"""
        if not self.is_exploding:  # Asegurarse de que no se reinicie la animación
            self.is_exploding = True
            self.explosion_frame_index = 0

    def update(self):
        """Actualiza cooldown de disparo y power-ups"""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        current_time = pygame.time.get_ticks()
        for powerup, end_time in list(self.powerup_timers.items()):
            if current_time > end_time:
                self.powerups[powerup] = False
                del self.powerup_timers[powerup]

                if powerup == "speed":
                    self.speed = 5

        # Actualizar la animación de explosión
        if self.is_exploding:
            if self.explosion_frame_index < len(self.explosion_frames):
                self.image = self.explosion_frames[self.explosion_frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.explosion_frame_index += 1
            else:
                self.kill()  # Elimina al jugador después de la animación de explosión

    def draw(self, screen):
        """Dibujar al jugador en pantalla"""
        screen.blit(self.image, self.rect)


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Cargar la imagen y girarla 90° si es necesario
        self.image = pygame.image.load("assets/FB00_nyknck/FB00_nyknck/FB001.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)  # Gira la imagen hacia arriba

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8  # Movimiento hacia arriba

    def update(self):
        """Mueve la bala hacia arriba y la elimina si sale de la pantalla"""
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()  # Elimina la bala si sale de la pantalla


# Función para mostrar el estado final cuando el jugador muere
def show_game_over(screen, score, level):
    font = pygame.font.SysFont('Arial', 48)  # Fuente para el texto
    text = font.render(f'Puntuación: {score}   Nivel: {level}', True, (255, 255, 255))  # Texto de puntuación y nivel
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centrar el texto en la pantalla
    screen.blit(text, text_rect)
    pygame.display.flip()


# Pausar el juego cuando el jugador muera
def pause_game():
    return True




