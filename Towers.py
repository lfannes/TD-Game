import pygame
import Position
import math

towerImage = pygame.image.load('images/tower.png')

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = Position.Position(self.x, self.y)
        self.damage = 1
        self.range = 200
        self.reload_ms = 500
        self.maxReload_ms = self.reload_ms
        self.hitbox = (self.position.x, self.position.y, towerImage.get_width(), towerImage.get_height())
        self.time = 0
        self.diff_ms = 0
        self.prev_ms = 0
        self.isFullAmmo = True

    def draw(self, screen, time):
        self.time = time * 1000
        self.diff_ms = self.time - self.prev_ms

        screen.blit(towerImage, (self.position.x, self.position.y))
        width = 104 - (104 / self.maxReload_ms * (self.maxReload_ms - self.reload_ms))
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 104, 10))
        pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 10))

        self.prev_ms = self.time
    def shoot(self, enemyList):
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


