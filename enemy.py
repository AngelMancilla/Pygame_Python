import pygame
import random

class Enemy(pygame.sprite.Sprite):
    """Clase base para todos los enemigos."""

    def __init__(self, x, y, speed, health, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, self.image.get_size())  # Ajusta el tamaño de la imagen
        self.rect = self.image.get_rect(topleft=(x, y))  # Define la posición inicial del enemigo
        self.speed = speed  # Velocidad del enemigo
        self.health = health  # Salud del enemigo

    def update(self):
        """Actualiza la posición del enemigo y reinicia su posición cuando sale de la pantalla."""
        self.rect.y += self.speed
        if self.rect.top > 600:  # Si el enemigo sale por la parte inferior de la pantalla
            self.rect.y = random.randint(-100, -40)  # Reinicia la posición de y
            self.rect.x = random.randint(50, 750)  # Asigna una posición aleatoria en el eje x

    def take_damage(self, amount):
        """Reduce la salud del enemigo al recibir daño. Si la salud es 0, elimina al enemigo."""
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Elimina al enemigo si su salud llega a cero


class EnemyFast(Enemy):
    """Enemigo rápido con baja salud."""

    def __init__(self, x, y):
        super().__init__(x, y, speed=7, health=30, image_path="assets/fast_enemy.png")

    def update(self):
        """Actualiza el movimiento del enemigo rápido."""
        super().update()  # Llama al método update de la clase base


class ShooterEnemy(Enemy):
    """Enemigo que dispara proyectiles."""

    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, speed=2, health=60, image_path="assets/shooter_enemy.png")
        self.bullet_group = bullet_group  # Grupo de balas donde se agregarán las balas disparadas
        self.shoot_timer = 0  # Temporizador para controlar el tiempo de disparo

    def update(self):
        """Actualiza el movimiento y el disparo del enemigo."""
        super().update()  # Llama al método update de la clase base
        self.shoot_timer += 1
        if self.shoot_timer > 120:  # Dispara cada 2 segundos (120 actualizaciones)
            self.shoot()
            self.shoot_timer = 0  # Reinicia el temporizador de disparo

    def shoot(self):
        """Genera una bala disparada por el enemigo."""
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)  # Crea una nueva bala
        self.bullet_group.add(bullet)  # Añade la bala al grupo de balas de los enemigos


class EnemyBullet(pygame.sprite.Sprite):
    """Bala disparada por los enemigos."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/FB00_nyknck/FB00_nyknck/FB001.png")
        self.image = pygame.transform.scale(self.image, (10, 20))  # Ajusta el tamaño de la bala
        self.rect = self.image.get_rect(center=(x, y))  # Establece la posición inicial de la bala
        self.speed = 4  # Velocidad de la bala

    def update(self):
        """Actualiza la posición de la bala del enemigo."""
        self.rect.y += self.speed  # Mueve la bala hacia abajo
        if self.rect.top > 600:  # Si la bala sale de la pantalla, se elimina
            self.kill()


# Función para generar enemigos aleatorios según el nivel
def spawn_enemy(level, bullet_group=None):
    """Genera enemigos con una variedad aleatoria según el nivel del juego."""
    # Selecciona aleatoriamente un tipo de enemigo
    enemy_type = random.choice([EnemyFast, ShooterEnemy])

    if enemy_type == EnemyFast:
        # Genera enemigos rápidos con un rango de posición aleatorio
        enemy = EnemyFast(random.randint(50, 750), random.randint(-100, -40))
    elif enemy_type == ShooterEnemy and bullet_group:
        # Genera enemigos que disparan con un rango de posición aleatorio
        enemy = ShooterEnemy(random.randint(50, 750), random.randint(-100, -40), bullet_group)

    return enemy

