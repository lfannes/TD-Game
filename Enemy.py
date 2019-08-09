import pygame
import Position


enemyImage1 = pygame.image.load('images/frame1.png')
enemyImage2 = pygame.image.load('images/frame2.png')

pathX = (45, 199, 199, 440, 440, 760, 760, 1200)
pathY = (436, 436, 209, 209, 520, 520, 373, 373)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.x = x
        self.y = y
        self.image = enemyImage1
        self.rect = self.image.get_rect()
        self.health = self.healthSwitch(self.type)
        print(f"type: {self.type}, health:{self.health}")
        self.maxHealth = self.health
        self.position = Position.Position(self.x, self.y)
        self.pos = self.position.copy()
        self.hitbox = (self.position.x, self.position.y, enemyImage1.get_width(), enemyImage1.get_height())
        self.time = 0
        self.isDead = False
        self.checkIsDead = True
        self.passedTime = 0

    def __repr__(self):
        return f"Position: {self.position}"

    def update(self, screen, diff_time):
        self.passedTime += (diff_time * 1000)
        self.draw(screen)

    def draw(self, screen):
        if not self.isDead:
            width = 50 - (50 / self.maxHealth * (self.maxHealth - self.health))
            self.hitbox = (self.position.x, self.position.y, enemyImage1.get_width(), enemyImage1.get_height())
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 50, 7))
            pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 7))
            self.position.x - 22.5, self.position.y - 22.5, enemyImage1.get_width(), enemyImage1.get_height()

            if self.passedTime < 500: #frame 1
                screen.blit(enemyImage1, (self.position.x, self.position.y))
            elif self.passedTime < 1000 and self.passedTime > 150: #frame 2
                screen.blit(enemyImage2, (self.position.x, self.position.y))
            else:
                self.passedTime = 0

    def move(self, pos):
        self.position.x = pos.x
        self.position.y = pos.y

    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
        if self.health <= 0:
            self.isDead = True
            return True
    def healthSwitch(self, i):
        switch = {
                1:100,
                2:150,
                3:200,
                4:300
        }
        return switch.get(i)