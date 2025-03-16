import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, health, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, self.image.get_size())
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = health

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(50, 750)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

class EnemyFast(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed = 7, health = 30, image_path="assets/fast_enemy.png")

    def update(self):
        super().update()

    def explode(self, player):
        player.take_damage(50)
        self.kill()

class ShooterEnemy(Enemy):
    def __init__(self, x, y, bullet_group):
        super().__init__(x, y, speed = 2, health = 60, image_path = "assets/shooter_enemy.png")
        self.bullet_group = bullet_group
        self.shoot_timer = 0

    def update(self):
        super().update()
        self.shoot_timer += 1
        if self.shoot_timer > 120:
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        self.bullet_group.add(bullet)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/FB00_nyknck/FB00_nyknck/FB001.png")
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()