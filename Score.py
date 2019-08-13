import pygame

myfont = pygame.font.Font('images/font.ttf', 50)

class Score:
    def __init__(self):
        self.score = 2500
        self.health = 20
        self.maxHealth = 20
        self.isDead = False

    def draw(self, screen):
        width = int(800 - (800 // self.maxHealth * (self.maxHealth - self.health)))
        pygame.draw.rect(screen, (255, 0, 0), (200, 650, 800, 15))
        pygame.draw.rect(screen, (0, 228, 0), (200, 650, width, 15))

        healthLabel = myfont.render(f"Health: {self.health}", 1, (169, 186, 203))
        screen.blit(healthLabel, (900, 35))

        scoreLabel = myfont.render(f"Score: {self.score}", 1, (169, 186, 203))
        screen.blit(scoreLabel, (900, 0))

    def hit(self, path, enemyList):
        for enemy in enemyList:
            if self.health <= 0:
                self.isDead = True
                break
            if path.max_time() - 2 <= enemy.time and not enemy.isDead:
                self.health -= 1
                enemy.isDead = True
                print("health - 1")