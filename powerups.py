import pygame
import random
from settings import *

class PowerUp(pygame.sprite.Sprite):
    """Clase base para los power-ups que caen en el juego."""

    def __init__(self, x, y, powerup_type):
        super().__init__()

        self.powerup_type = powerup_type  # Tipo de power-up (velocidad, escudo, daño)

        # Cargar las imágenes para cada tipo de power-up
        self.images = {
            "speed": pygame.image.load("assets/powerup_speed.png").convert_alpha(),
            "shield": pygame.image.load("assets/powerup_shield.png").convert_alpha(),
            "damage": pygame.image.load("assets/powerup_damage.png").convert_alpha(),
        }

        # Redimensionar todas las imágenes a un tamaño adecuado
        for key in self.images:
            self.images[key] = pygame.transform.scale(self.images[key], (40, 40))

        # Asignar la imagen correspondiente según el tipo de power-up
        self.image = self.images[powerup_type]
        self.rect = self.image.get_rect(center=(x, y))  # Establece la posición inicial

        self.speed = 2  # Velocidad con la que el power-up cae hacia abajo

    def update(self):
        """Actualiza la posición del power-up y elimina el power-up si sale de la pantalla."""
        self.rect.y += self.speed  # Desplazamiento hacia abajo

        if self.rect.top > HEIGHT:  # Si el power-up sale de la pantalla
            self.kill()  # Elimina el power-up del grupo de sprites
