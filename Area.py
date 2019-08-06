import pygame
import Position

pathImage = pygame.image.load('images/path.png')

class Area(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = Position.Position(0, 0)
        self.image = pathImage
        self.rect = self.image.get_rect()

    def update(self, screen, a=None, b=None):
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def isClear(self, obj, group):
        collision = pygame.sprite.spritecollide(obj, group, False)
        print(collision)
        if collision:
            return True
