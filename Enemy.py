import pygame
import Position
import util

enemyImage1 = pygame.image.load('images/e10.png')
enemyImage1 = pygame.transform.scale(enemyImage1, (enemyImage1.get_width()*3, enemyImage1.get_height()*3))
enemyImage2 = pygame.image.load('images/e11.png')
enemyImage2 = pygame.transform.scale(enemyImage2, (enemyImage2.get_width()*3, enemyImage2.get_height()*3))
enemy1Images = [pygame.image.load('images/e10.png'), pygame.image.load('images/e11.png'), pygame.image.load('images/e12.png'), pygame.image.load('images/e13.png'), pygame.image.load('images/e14.png'), pygame.image.load('images/e15.png')]
enemy1Images = util.scale(enemy1Images, 3)

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
        self.health = self.healthSwitch()
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
            elif self.passedTime < 1000: #frame 2
                screen.blit(enemyImage2, (self.position.x, self.position.y))
            else:
                self.passedTime = 0
            self.drawAnimation(screen)


    def move(self, pos):
        self.position.x = pos.x
        self.position.y = pos.y

    def hit(self, damage):
        if self.health > 0:
            self.health -= damage
        if self.health <= 0:
            self.isDead = True
            return True
    def healthSwitch(self):
        switch = {
                1:100,
                2:150,
                3:200,
                4:300
        }
        return switch.get(self.type)

    def drawAnimation(self, screen):
        imageList = "enemy" + self.type + "Images"
        if self.passedTime < 500:
            screen.blit(vars(imageList), (100, 100))

        elif self.passedTime < 1000:
            pass

        elif self.passedTime < 1000:
            pass

        elif self.passedTime < 1000:
            pass

        elif self.passedTime < 1000:
            pass

        elif self.passedTime < 1000:
            pass
