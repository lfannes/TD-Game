import pygame
import Position
import math

towerImage = pygame.image.load('images/tower.png')

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.position = Position.Position(self.x, self.y)
        self.image = towerImage
        self.rect = self.image.get_rect()
        self.rect.center = (self.position.x + 51, self.position.y + 81.5)
        self.damage = 50
        self.range = 200
        self.reload_ms = 500
        self.maxReload_ms = self.reload_ms
        self.hitbox = (self.position.x, self.position.y, towerImage.get_width(), towerImage.get_height())
        self.time = 0
        self.diff_ms = 0
        self.prev_ms = 0
        self.isFullAmmo = True

    def placing(self, screen, alpha, pos):
        self.rect.center = (self.position.x + 51, self.position.y + 81.5)
        pygame.draw.circle(screen, (24, 204, 255), (pos[0] + 52, pos[1] + 81), self.range, 5)
        self.position = Position.Position(pos[0], pos[1])
        self.draw(screen, alpha)

    def place(self, pos):
        self.position = Position.Position(pos[0] - 52, pos[1] - 81.5)

    def update(self, screen, enemyList, time):
        self.rect.center = (self.position.x + 51, self.position.y + 81.5)
        self.shoot(enemyList, time)
        self.draw(screen)

    def draw(self, screen, alpha=255):
        self.hitbox = (self.position.x, self.position.y, towerImage.get_width(), towerImage.get_height())
        blit_alpha(screen, towerImage, (self.position.x, self.position.y), alpha)
        width = 104 - (104 / self.maxReload_ms * (self.maxReload_ms - self.reload_ms))
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 104, 10))
        pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 10))

        self.prev_ms = self.time

    def shoot(self, enemyList, time):
        self.time = time * 1000
        self.diff_ms = self.time - self.prev_ms
        if self.isFullAmmo:
            for enemy in enemyList:
                distance = self.position.distance(enemy.position, self.image)
                print(distance)
                if distance <= self.range and not enemy.isDead:
                    enemy.hit(self.damage)
                    self.isFullAmmo = False
                    self.reload_ms = 0
                    break
        else:
            self.reload_ms += self.diff_ms
            if self.reload_ms >= self.maxReload_ms:
                self.isFullAmmo = True

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

if __name__ == '__main__':
    tower = Tower(50, 30)
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('TD Game')
    while True:
        tower.position = Position.Position(500, 400)
        tower.draw(screen)
        pygame.display.update()