import pygame
import Position

polygonCordinate = ((0, 395))
polygonLength = (pygame.Surface((150, 70)))
pathImage = pygame.image.load('images/path.png')

class Area(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = Position.Position(0, 0)
        self.image = pathImage
        self.rect = self.image.get_rect()
        self.rect.center = (600, 400)

    def update(self, screen, a=None, b=None):
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def isClear(self, obj, group):
        collision = pygame.sprite.collide_mask(obj, group)
        #print(collision)
        if collision:
            print("collision")
            return True
        else:
            return False


