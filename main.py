import pygame
from settings import *
from player import Player

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Python')

clock = pygame.time.Clock()

bg = pygame.image.load("assets/bg_space.png")
player = Player(WIDTH / 2, HEIGHT - 60)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    all_sprites.update()

    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
