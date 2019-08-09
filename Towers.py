import pygame
import Position
import util

pygame.init()

myfont = pygame.font.Font('images/font.ttf', 50)

towerImageLoad = pygame.image.load('images/tower11.png')
towerImageLoad = pygame.transform.scale(towerImageLoad, (100, 100))

towerImageEmpty = pygame.image.load('images/tower10.png')
towerImageEmpty = pygame.transform.scale(towerImageEmpty, (100, 100))

upgrade = pygame.image.load('images/upgrade.png')
upgrade = pygame.transform.scale(upgrade, (48, 48))

sell = pygame.image.load('images/sell.png')
sell = pygame.transform.scale(sell, (48, 48))

replace = pygame.image.load('images/replace.png')
replace = pygame.transform.scale(replace, (48, 48))


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.position = Position.Position(self.x, self.y)
        self.image = towerImageLoad
        self.rect = self.image.get_rect()
        self.rect.center = (self.position.x + 50, self.position.y + 50)
        self.damage = 50
        self.range = 200
        self.reload_ms = 500
        self.maxReload_ms = self.reload_ms
        self.hitbox = (self.position.x, self.position.y, towerImageLoad.get_width(), towerImageLoad.get_height())
        self.time = 0
        self.diff_ms = 0
        self.prev_ms = 0
        self.isFullAmmo = True
        self.isMenuVisible = False
        self.upgradeRect = upgrade.get_rect()
        self.sellRect = upgrade.get_rect()
        self.replaceRect = upgrade.get_rect()
        self.upgradeCount = 0
        self.upgradeCost = (50, 80, 120)
        self.extaDamage = (25, 30, 50)
        self.startTimer = False
        self.timer = 0
        self.label = None
        self.label2 = None

    def placing(self, screen, alpha, pos, collision):
        self.rect.center = (self.position.x + 50, self.position.y + 50)
        self.position = Position.Position(pos[0], pos[1])
        if collision:
            pygame.draw.circle(screen, (255, 24, 24, 180), self.rect.center, self.range)
        else:
            pygame.draw.circle(screen, (24, 255, 24, 180), self.rect.center, self.range)
        self.draw(screen, alpha)

    def place(self, pos):
        self.position = Position.Position(pos[0] - 50, pos[1] - 50)

    def update(self, screen, enemyList, time, diff_time, a=None):
        self.rect.center = (self.position.x + 50, self.position.y + 50)
        self.shoot(enemyList, time)
        self.draw(screen, diff_time)

    def draw(self, screen, diff_time, alpha=255):
        self.hitbox = (self.position.x, self.position.y, towerImageLoad.get_width(), towerImageLoad.get_height())

        if self.isFullAmmo:
            blit_alpha(screen, towerImageLoad, (self.position.x, self.position.y), alpha)
        elif self.reload_ms >= self.maxReload_ms - 150:
            blit_alpha(screen, towerImageLoad, (self.position.x, self.position.y), alpha)
        else:
            blit_alpha(screen, towerImageEmpty, (self.position.x, self.position.y), alpha)

        if not self.isMenuVisible:
            width = 100 - (100 / self.maxReload_ms * (self.maxReload_ms - self.reload_ms))
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, 100, 10))
            pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 10))

        if self.isMenuVisible:
            self.selectMenu(screen)

        if self.startTimer:
            screen.blit(self.label, (300, 50))
            if self.label2:
                screen.blit(self.label2, (300, 85))
            self.timer += diff_time
            print(self.timer)
            if self.timer >= 2.5:
                self.startTimer = False
                self.timer = 0
                self.label2 = None

        self.prev_ms = self.time

    def shoot(self, enemyList, time):
        self.time = time * 1000
        self.diff_ms = self.time - self.prev_ms
        if self.isFullAmmo:
            for enemy in enemyList:
                distance = self.position.distance(enemy.position, self.image)
                if distance <= self.range and not enemy.isDead:
                    enemy.hit(self.damage)
                    self.isFullAmmo = False
                    self.reload_ms = 0
                    break
        else:
            self.reload_ms += self.diff_ms
            if self.reload_ms >= self.maxReload_ms:
                self.isFullAmmo = True

    def selected(self):
        print("selected")
        if not self.isMenuVisible:
            self.isMenuVisible = True
        else:
            self.isMenuVisible = False

    def selectMenu(self, screen):
        # draw
        screen.blit(upgrade, (self.position.x + towerImageLoad.get_width() / 2 - upgrade.get_width() / 2, self.position.y + towerImageLoad.get_width() / 2 - 125)) #draw the upgrade
        self.upgradeRect.topleft = (self.position.x + towerImageLoad.get_width() / 2 - upgrade.get_width() / 2, self.position.y + towerImageLoad.get_width() / 2 - 125)

        screen.blit(sell, (self.position.x + towerImageLoad.get_width() / 2 - upgrade.get_width() / 2 ,self.position.y + towerImageLoad.get_width() / 2 + 77))  # draw the upgrade
        self.sellRect.topleft = (self.position.x + towerImageLoad.get_width() / 2 - upgrade.get_width() / 2,self.position.y + towerImageLoad.get_width() / 2 + 77)

    def towerActions(self, screen, mousePos, game, pressed):
        if util.pressedImage(mousePos, self.hitbox):
                #when the tower is pressed
                print("pressed the tower")
                self.selected()

        elif util.pressedImage(mousePos, self.upgradeRect):
                #when upgrade is presssed
                print("pressed upgrade")
                print(pressed)
                if pressed[0]:
                    try:
                        if game.score.score >= self.upgradeCost[self.upgradeCount]:
                            self.damage += 25
                            game.score.score -= self.upgradeCost[self.upgradeCount]
                            self.upgradeCount += 1

                            self.label = myfont.render(f"Upgrade succeed", False, (51, 255, 51))
                            screen.blit(self.label, (300, 50))
                            self.startTimer = True

                        else:
                            self.label = myfont.render("You don't have enough money", False, (255, 51, 51))
                            screen.blit(self.label, (300, 50))
                            self.startTimer = True
                    except IndexError:
                        self.label = myfont.render("Your tower is fully upgraded", False, (255, 51, 51))
                        screen.blit(self.label, (300, 50))
                        self.startTimer = True

                elif pressed[2]:
                    try:
                        self.label = myfont.render(f"cost: {self.upgradeCost[self.upgradeCount]}", False, (51, 255, 51))
                        self.label2 = myfont.render(f"damage: {self.damage + 25}", False, (51, 255, 51))

                        screen.blit(self.label, (300, 50))
                        screen.blit(self.label2, (300, 85))

                        self.startTimer = True
                    except IndexError:
                        self.label = myfont.render("Your tower is fully upgraded", False, (255, 51, 51))
                        screen.blit(self.label, (300, 50))
                        self.startTimer = True


        elif util.pressedImage(mousePos, self.sellRect):
                #when sell is pressed
                print("pressed sell")


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