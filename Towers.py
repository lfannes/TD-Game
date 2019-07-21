import pygame
import Position

towerImage = pygame.image.load('images/tower.png')

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = Position.Position(self.x, self.y)

    def draw(self, screen):
        screen.blit(towerImage, (self.position.x, self.position.y))

