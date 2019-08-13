import pygame


background = pygame.image.load('images/background.png')

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = background
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))