import pygame
import Position
import util


enemy1Images = [pygame.image.load('images/e10.png'), pygame.image.load('images/e11.png'), pygame.image.load('images/e12.png'), pygame.image.load('images/e13.png'), pygame.image.load('images/e14.png'), pygame.image.load('images/e15.png')]
enemy1Images = util.scaleList(enemy1Images, 3)

enemy2Images = [pygame.image.load('images/e20.png'), pygame.image.load('images/e21.png'), pygame.image.load('images/e22.png'), pygame.image.load('images/e23.png'), pygame.image.load('images/e24.png'), pygame.image.load('images/e25.png')]
enemy2Images = util.scaleList(enemy2Images, 3)

enemy3Images = [pygame.image.load('images/e30.png'), pygame.image.load('images/e31.png'), pygame.image.load('images/e32.png'), pygame.image.load('images/e33.png'), pygame.image.load('images/e34.png'), pygame.image.load('images/e35.png')]
enemy3Images = util.scaleList(enemy3Images, 3)

enemy4Images = [pygame.image.load('images/e40.png'), pygame.image.load('images/e41.png'), pygame.image.load('images/e42.png'), pygame.image.load('images/e43.png'), pygame.image.load('images/e44.png'), pygame.image.load('images/e45.png')]
enemy4Images = util.scaleList(enemy4Images, 3)

pathX = (45, 199, 199, 440, 440, 760, 760, 1200)
pathY = (436, 436, 209, 209, 520, 520, 373, 373)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.image = self.getAnimationImages()
        self.image = self.image[0]
        self.rect = self.image.get_rect()
        self.health = self.healthSwitch()
        print(f"type: {self.type}, health:{self.health}")
        self.maxHealth = self.health
        self.position = Position.Position(0, 0)
        self.pos = self.position.copy()
        self.hitbox = (self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
        self.time = 0
        self.isDead = False
        self.checkIsDead = True
        self.passedTime = 0
        self.enemyImages = self.getAnimationImages()
        self.score = self.getScore()

    def __repr__(self):
        return f"Position: {self.position}"

    def update(self, screen, diff_time):
        self.passedTime += (diff_time * 1000)
        self.draw(screen)

    def draw(self, screen):
        if not self.isDead:
            width = 50 - (50 / self.maxHealth * (self.maxHealth - self.health))
            self.hitbox = (self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 50, 7))
            pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 7))
            self.position.x - 22.5, self.position.y - 22.5, self.image.get_width(), self.image.get_height()

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
                1:150,
                2:200,
                3:300,
                4:500
        }
        return switch.get(self.type)

    def getAnimationImages(self):
        if self.type == 1:
             return enemy1Images
        elif self.type == 2:
            return enemy2Images
        elif self.type == 3:
            return enemy3Images
        elif self.type == 4:
            return enemy4Images
        else:
            return False

    def getScore(self):
        if self.type == 1:
             return 5
        elif self.type == 2:
            return 10
        elif self.type == 3:
            return 15
        elif self.type == 4:
            return 20
        else:
            return False

    def drawAnimation(self, screen):
        speed = 300
        if self.passedTime < speed:
            screen.blit(self.enemyImages[0], (self.position.x, self.position.y))

        elif self.passedTime < speed*2:
            screen.blit(self.enemyImages[1], (self.position.x, self.position.y))

        elif self.passedTime < speed*3:
            screen.blit(self.enemyImages[2], (self.position.x, self.position.y))

        elif self.passedTime < speed*4:
            screen.blit(self.enemyImages[3], (self.position.x, self.position.y))

        elif self.passedTime < speed*5:
            screen.blit(self.enemyImages[4], (self.position.x, self.position.y))

        elif self.passedTime < speed*6:
            screen.blit(self.enemyImages[5], (self.position.x, self.position.y))
        else:
            self.passedTime = 0
