import pygame
import Position
import math

towerImage = pygame.image.load('images/tower.png')

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = towerImage
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.position = Position.Position(self.x, self.y)
        self.damage = 50
        self.range = 200
        self.reload_ms = 500
        self.maxReload_ms = self.reload_ms
        self.hitbox = (self.position.x, self.position.y, towerImage.get_width(), towerImage.get_height())
        self.time = 0
        self.diff_ms = 0
        self.prev_ms = 0
        self.isFullAmmo = True

    def update(self, screen, enemyList, time):
        self.shoot(enemyList, time)
        self.draw(screen)

    def draw(self, screen):
        print(f"x: {self.x}, y: {self.y}")
        self.hitbox = (self.position.x, self.position.y, towerImage.get_width(), towerImage.get_height())
        screen.blit(self.image, (self.position.x, self.position.y))
        width = 104 - (104 / self.maxReload_ms * (self.maxReload_ms - self.reload_ms))
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 104, 10))
        pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 10))



        self.prev_ms = self.time
    def shoot(self, enemyList, time):
        self.time = time * 1000
        self.diff_ms = self.time - self.prev_ms
        if self.isFullAmmo:
            for enemy in enemyList:
                distance = self.position.distance(enemy.position)
                if distance <= self.range and not enemy.isDead:
                    enemy.hit(self.damage)
                    self.isFullAmmo = False
                    self.reload_ms = 0
                    break
        else:
            self.reload_ms += self.diff_ms
            if self.reload_ms >= self.maxReload_ms:
                self.isFullAmmo = True


if __name__ == '__main__':
    tower = Tower(50, 30)
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption('TD Game')
    while True:
        tower.position = Position.Position(500, 400)
        tower.draw(screen)
        pygame.display.update()