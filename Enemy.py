import pygame
import Position

enemyImage = pygame.image.load('images/enemy.png')

pathX = (45, 199, 199, 440, 440, 760, 760, 1200)
pathY = (436, 436, 209, 209, 520, 520, 373, 373)

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.maxHealth = 100
        self.position = Position.Position(self.x, self.y)
        self.pos = self.position.copy()
        self.hitbox = (self.position.x, self.position.y, enemyImage.get_width(), enemyImage.get_height())
        self.time = 0

    def __repr__(self):
        return f"Position: {self.position}"

    def draw(self, screen):

        width = 50 - (50 / self.maxHealth * (self.maxHealth - self.health))
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 50, 7))
        pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 7))
        self.hitbox = (self.position.x, self.position.y, enemyImage.get_width(), enemyImage.get_height())
        self.position.x - 22.5, self.position.y - 22.5, enemyImage.get_width(), enemyImage.get_height()

        screen.blit(enemyImage, (self.position.x, self.position.y))

    def move(self, pos):
        self.position.x = pos.x
        self.position.y = pos.y