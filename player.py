import pygame
from settings import *
from powerups import PowerUp

class Player(pygame.sprite.Sprite):
    """Clase que representa al jugador."""

    def __init__(self, x, y, bullet_group, powerup_group, shoot_sound, damage_sound):
        super().__init__()

        # Cargar la imagen del jugador
        self.original_image = pygame.image.load('assets/player_ship.png').convert_alpha()
        self.image = self.original_image
        self.image.set_colorkey((0, 0, 0))  # Define el color transparente

        self.rect = self.image.get_rect(center=(x, y))  # Establece la posición inicial

        # Atributos del jugador
        self.speed = 5
        self.health = 100
        self.level = 1
        self.score = 0

        # Grupos para las balas y power-ups
        self.bullet_group = bullet_group
        self.powerup_group = powerup_group
        self.shoot_cooldown = 0

        # Sonidos
        self.shoot_sound = shoot_sound
        self.damage_sound = damage_sound

        # Power-ups del jugador
        self.powerups = {
            "speed": False,
            "shield": False,
            "damage": False,
        }
        self.powerup_timers = {}

        # Animación de explosión
        self.explosion_frames = self.load_explosion_frames()
        self.explosion_frame_index = 0
        self.is_exploding = False

    def load_explosion_frames(self):
        """Carga los fotogramas de la animación de explosión."""
        frames = []
        for i in range(1, 6):
            frames.append(pygame.image.load(f'assets/FB00_nyknck/FB00_nyknck/FB00{i}.png').convert_alpha())
        return frames

    def move(self, keys):
        """Mueve al jugador según las teclas presionadas."""
        if self.is_exploding:
            return  # No se mueve durante la explosión

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        """Dispara una bala si no está en cooldown."""
        if self.shoot_cooldown == 0:
            bullet = PlayerBullet(self.rect.centerx, self.rect.top)  # Crea la bala
            self.bullet_group.add(bullet)  # La añade al grupo de balas
            self.shoot_sound.play()  # Reproduce el sonido de disparo
            self.shoot_cooldown = 10 if self.powerups["damage"] else 15  # Reducir el tiempo de cooldown si el powerup de daño está activo

    def take_damage(self, amount):
        """Reduce la salud del jugador si no tiene un escudo activo."""
        if not self.powerups["shield"]:
            self.health -= amount
            self.damage_sound.play()  # Reproduce el sonido de daño
        if self.health <= 0:
            self.explode()  # Inicia la animación de explosión

    def explode(self):
        """Inicia la animación de explosión cuando la salud llega a 0."""
        if not self.is_exploding:
            self.is_exploding = True
            self.explosion_frame_index = 0

    def activate_powerup(self, powerup_type, duration=5000):
        """Activa un power-up con una duración limitada."""
        self.powerups[powerup_type] = True
        self.powerup_timers[powerup_type] = pygame.time.get_ticks() + duration

        # Efectos de cada power-up
        if powerup_type == "speed":
            self.speed = 8  # Aumenta la velocidad
        elif powerup_type == "shield":
            self.powerups["shield"] = True  # Activa el escudo
        elif powerup_type == "damage":
            self.shoot_cooldown = 5  # Dispara más rápido

    def update(self):
        """Actualiza la lógica del jugador, incluyendo el manejo de power-ups y la explosión."""
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1  # Reducir el cooldown del disparo

        current_time = pygame.time.get_ticks()
        for powerup, end_time in list(self.powerup_timers.items()):
            if current_time > end_time:  # Si el powerup ha expirado
                self.powerups[powerup] = False  # Desactívalo
                del self.powerup_timers[powerup]

                # Restablecer valores después de que el powerup termine
                if powerup == "speed":
                    self.speed = 5
                elif powerup == "damage":
                    self.shoot_cooldown = 15

        # Detecta si el jugador colisiona con power-ups
        powerup_hit = pygame.sprite.spritecollide(self, self.powerup_group, True)
        for powerup in powerup_hit:
            self.activate_powerup(powerup.powerup_type)

        # Maneja la animación de explosión
        if self.is_exploding:
            if self.explosion_frame_index < len(self.explosion_frames):
                self.image = self.explosion_frames[self.explosion_frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)
                self.explosion_frame_index += 1
            else:
                self.kill()  # Elimina al jugador después de la animación de explosión

    def draw(self, screen):
        """Dibuja la imagen del jugador en la pantalla."""
        screen.blit(self.image, self.rect)


class PlayerBullet(pygame.sprite.Sprite):
    """Clase para las balas disparadas por el jugador."""

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("assets/FB00_nyknck/FB00_nyknck/FB001.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)  # Rota la bala para que apunte hacia arriba

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8  # Velocidad de la bala hacia arriba

    def update(self):
        """Actualiza la posición de la bala y la elimina si sale de la pantalla."""
        self.rect.y += self.speed
        if self.rect.bottom < 0:  # Si la bala sale de la pantalla
            self.kill()  # La elimina

