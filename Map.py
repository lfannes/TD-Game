import pygame

background = pygame.image.load('images/background.png')

class Map:
    def __init__(self):
        pass

    def draw(self, screen):
        screen.blit(background, (0, 0))