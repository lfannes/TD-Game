import pygame
import Position

pathImage = pygame.image.load('images/path.png')

class Area(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.position = Position.Position(0, 0)
        self.image = pathImage
        self.rect = self.image.get_rect()
        self.rect.center = (600, 400)

    def update(self, screen):
        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.image, (self.position.x, self.position.y))

    def isClear(self, obj, path, map, tower):
        pathCollision = pygame.sprite.collide_mask(obj, path)
        mapCollsion = pygame.sprite.collide_mask(obj, map)
        if tower:
            towerCollsion = pygame.sprite.collide_circle(obj, tower)
        else:
            towerCollsion = None

        print(f"map: {mapCollsion}")
        print(f"path: {pathCollision}")
        print(f"tower: {towerCollsion}")

        if not pathCollision and  not towerCollsion and mapCollsion:
            print("true")
            return True
        else:
            print("false")
            return False




if __name__ == '__main__':
    area = Area()
    path = pygame.sprite.collide_mask()