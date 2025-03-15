import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.original_image = pygame.image.load('assets/tiny_ship20.png').convert_alpha()
        self.image = self.original_image
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = 5
        self.health = 100
        self.level = 1

        self.direction = "UP"

        self.powerups = {
            "speed": False,
            "shield": False,
            "damage": False,
        }
        self.powerup_timers = {}

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "LEFT"
            self.update_image()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "RIGHT"
            self.update_image()

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = "UP"
            self.update_image()

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = "DOWN"
            self.update_image()

    def update_image(self):
        if self.direction == "UP":
            self.image = self.original_image
        elif self.direction == "DOWN":
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == "LEFT":
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == "RIGHT":
            self.image = pygame.transform.rotate(self.original_image, -90)

        self.rect = self.image.get_rect(center=self.rect.center)

    def take_damage(self, amount):
        if not self.powerups["shield"]:
            self.health -= amount
        if self.health <= 0:
            print("¡Jugador eliminado!")

    def apply_powerups(self, type, duration):
        self.powerups[type] = True
        self.powerup_timers[type] = pygame.time.get_ticks() + duration

        if type == "speed":
            self.speed = 10

    def update(self):
        current_time = pygame.time.get_ticks()

        for powerup, end_time in list(self.powerup_timers.items()):
            if current_time > end_time:
                self.powerups[powerup] = False
                del self.powerup_timers[powerup]

                if powerup == "speed":
                    self.speed = 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)

