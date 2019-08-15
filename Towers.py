import pygame
import Position
import util
import time

pygame.init()

myfont = pygame.font.Font('images/font.ttf', 50)

tower1 = [pygame.image.load('images/tower20.png'), pygame.image.load('images/tower21.png')]
tower1 = util.scaleList(tower1, 2)

tower11 = [pygame.image.load('images/tower22.png'), pygame.image.load('images/tower23.png')]
tower11 = util.scaleList(tower11, 2)

tower2 = [pygame.image.load('images/tower30.png'), pygame.image.load('images/tower30.png')]
tower2 = util.scaleList(tower2, 2)

tower21 = [pygame.image.load('images/tower31.png'), pygame.image.load('images/tower31.png')]
tower21 = util.scaleList(tower21, 2)

upgrade = pygame.image.load('images/upgrade.png')
upgrade = util.scaleSingleImage(upgrade, 0.75)

sell = pygame.image.load('images/sell.png')
sell = util.scaleSingleImage(sell, 0.75)

replace = pygame.image.load('images/replace.png')
replace = util.scaleSingleImage(replace, 0.75)


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.position = Position.Position(self.x, self.y)
        self.image = tower1[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.position.x + 50, self.position.y + 50)
        self.damage = 0
        self.range = 150
        self.reload_ms = 500
        self.maxReload_ms = self.reload_ms
        self.hitbox = (self.position.x, self.position.y, self.image.get_width(), self.image.get_height())
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
        self.extaDamage = (25, 30, 60)
        self.startTimer = False
        self.timer = 0
        self.label = None
        self.type = 0
        self.maxUpgraded = False

    def placing(self, screen, alpha, pos, collision, type):
        self.type = type
        self.damage = self.getDamage(self.type)
        self.position = Position.Position(pos[0], pos[1])
        self.rect.center = (self.position.x + self.image.get_width() / 2, self.position.y + self.image.get_height() / 2)
        print("placing")
        if collision:
            pygame.draw.circle(screen, (24, 255, 24, 180), self.rect.center, self.range)
            print(self.rect.center)
            print("green")
        else:
            print("red")
            pygame.draw.circle(screen, (255, 24, 24, 180), self.rect.center, self.range)
        self.draw(screen, None, alpha)

    def place(self, pos):
        self.position = Position.Position(pos[0] - 50, pos[1] - 50)

    def update(self, screen, enemyList, time, diff_time, a=None):
        self.rect.center = (self.position.x + self.image.get_width() / 2, self.position.y + self.image.get_height() / 2)
        self.shoot(enemyList, time)
        self.draw(screen, diff_time)

    def draw(self, screen, diff_time, alpha=255):
        if self.isMenuVisible:
            self.selectMenu(screen)

        self.image = self.getAnimationImages()[1]
        self.hitbox = (self.position.x, self.position.y, self.image.get_width(), self.image.get_height())

        if self.type == 1:
            if self.isFullAmmo:
                blit_alpha(screen, tower1[1], (self.position.x, self.position.y), alpha)
            elif self.reload_ms >= self.maxReload_ms - 150:
                blit_alpha(screen, tower1[1], (self.position.x, self.position.y), alpha)
            else:
                blit_alpha(screen, tower1[0], (self.position.x, self.position.y), alpha)
        elif self.type == 1.1:
            self.image = self.getAnimationImages()[1]
            self.hitbox = (self.position.x, self.position.y, self.image.get_width(), self.image.get_height())

            if self.isFullAmmo:
                blit_alpha(screen, tower11[1], (self.position.x, self.position.y), alpha)
            elif self.reload_ms >= self.maxReload_ms - 150:
                blit_alpha(screen, tower11[1], (self.position.x, self.position.y), alpha)
            else:
                blit_alpha(screen, tower11[0], (self.position.x, self.position.y), alpha)
        elif self.type == 2:
            if self.isFullAmmo:
                blit_alpha(screen, tower2[1], (self.position.x, self.position.y), alpha)
            elif self.reload_ms >= self.maxReload_ms - 150:
                blit_alpha(screen, tower2[1], (self.position.x, self.position.y), alpha)
            else:
                blit_alpha(screen, tower2[0], (self.position.x, self.position.y), alpha)
        elif self.type == 2.1:
            if self.isFullAmmo:
                blit_alpha(screen, tower21[1], (self.position.x, self.position.y), alpha)
            elif self.reload_ms >= self.maxReload_ms - 150:
                blit_alpha(screen, tower21[1], (self.position.x, self.position.y), alpha)
            else:
                blit_alpha(screen, tower21[0], (self.position.x, self.position.y), alpha)

        if not self.isMenuVisible:
            width = self.image.get_width() - (
                        self.image.get_width() / self.maxReload_ms * (self.maxReload_ms - self.reload_ms))
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, self.image.get_width(), 10))
            pygame.draw.rect(screen, (0, 228, 0), (self.hitbox[0], self.hitbox[1] - 15, width, 10))

        if self.startTimer:
            screen.blit(self.label, (300, 50))
            self.timer += diff_time
            print(self.timer)
            if self.timer >= 2.5:
                self.startTimer = False
                self.timer = 0

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
        if self.isMenuVisible:
            pygame.draw.circle(screen, (192, 192, 192, 80), self.rect.center, self.range)

        if self.type == 1:
            screen.blit(upgrade, (self.position.x + tower1[1].get_width() / 2 - upgrade.get_width() / 2,
                                  self.position.y + tower1[1].get_width() / 2 - 125))  # draw the upgrade
            self.upgradeRect.topleft = (self.position.x + tower1[1].get_width() / 2 - upgrade.get_width() / 2,
                                        self.position.y + tower1[1].get_width() / 2 - 125)

            screen.blit(sell, (self.position.x + tower1[1].get_width() / 2 - upgrade.get_width() / 2,
                               self.position.y + tower1[1].get_width() / 2 + 77))  # draw the upgrade
            self.sellRect.topleft = (self.position.x + tower1[1].get_width() / 2 - upgrade.get_width() / 2,
                                     self.position.y + tower1[1].get_width() / 2 + 77)
        elif self.type == 1.1:
            screen.blit(upgrade, (self.position.x + tower11[1].get_width() / 2 - upgrade.get_width() / 2,
                                  self.position.y + tower11[1].get_width() / 2 - 125))  # draw the upgrade
            self.upgradeRect.topleft = (self.position.x + tower11[1].get_width() / 2 - upgrade.get_width() / 2, self.position.y + tower11[1].get_width() / 2 - 125)

            screen.blit(sell, (self.position.x + tower11[1].get_width() / 2 - upgrade.get_width() / 2,
                               self.position.y + tower11[1].get_width() / 2 + 77))  # draw the upgrade
            self.sellRect.topleft = (self.position.x + tower11[1].get_width() / 2 - upgrade.get_width() / 2,
                                     self.position.y + tower11[1].get_width() / 2 + 77)
        elif self.type == 2:
            screen.blit(upgrade, (self.position.x + tower2[1].get_width() / 2 - upgrade.get_width() / 2,
                                  self.position.y + tower2[1].get_width() / 2 - 125))  # draw the upgrade
            self.upgradeRect.topleft = (self.position.x + tower2[1].get_width() / 2 - upgrade.get_width() / 2, self.position.y + tower2[1].get_width() / 2 - 125)

            screen.blit(sell, (self.position.x + tower2[1].get_width() / 2 - upgrade.get_width() / 2,
                               self.position.y + tower2[1].get_width() / 2 + 77))  # draw the upgrade
            self.sellRect.topleft = (self.position.x + tower2[1].get_width() / 2 - upgrade.get_width() / 2,
                                     self.position.y + tower2[1].get_width() / 2 + 77)
        elif self.type == 2.1:
            screen.blit(upgrade, (self.position.x + tower21[1].get_width() / 2 - upgrade.get_width() / 2,
                                  self.position.y + tower21[1].get_width() / 2 - 125))  # draw the upgrade
            self.upgradeRect.topleft = (self.position.x + tower21[1].get_width() / 2 - upgrade.get_width() / 2, self.position.y + tower21[1].get_width() / 2 - 125)

            screen.blit(sell, (self.position.x + tower21[1].get_width() / 2 - upgrade.get_width() / 2,
                               self.position.y + tower21[1].get_width() / 2 + 77))  # draw the upgrade
            self.sellRect.topleft = (self.position.x + tower21[1].get_width() / 2 - upgrade.get_width() / 2,
                                     self.position.y + tower21[1].get_width() / 2 + 77)

    def upgrade(self, screen, game):
        if self.type == 1:
            if game.score.score >= self.getPrice(self.type):
                self.type = 1.1
                self.damage = self.getDamage(self.type)
                game.score.score -= self.getPrice(self.type)
                self.image = self.getAnimationImages()[1]

                self.label = myfont.render(f"Upgrade succeed", False, (51, 255, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
            else:
                self.label = myfont.render("You don't have enough money", False, (255, 51, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
        elif self.type == 1.1 and not self.maxUpgraded:
            if game.score.score >= self.getPrice(self.type):
                self.maxReload_ms = 400

                self.label = myfont.render(f"Upgrade succeed", False, (51, 255, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
                self.maxUpgraded = True
            else:
                self.label = myfont.render("You don't have enough money", False, (255, 51, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
        elif self.type == 2:
            if game.score.score >= self.getPrice(self.type):
                self.type = 2.1
                self.damage = self.getDamage(self.type)
                game.score.score -= self.getPrice(self.type)
                self.image = self.getAnimationImages()[1]

                self.label = myfont.render(f"Upgrade succeed", False, (51, 255, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
            else:
                self.label = myfont.render("You don't have enough money", False, (255, 51, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
        elif self.type == 2.1 and not self.maxUpgraded:
            if game.score.score >= self.getPrice(self.type):
                self.maxReload_ms = 300
                self.maxUpgraded = True

                self.label = myfont.render(f"Upgrade succeed", False, (51, 255, 51))
                screen.blit(self.label, (300, 50))
                self.startTimer = True
        else:
            self.label = myfont.render("Your tower is fully upgraded", False, (255, 51, 51))
            screen.blit(self.label, (300, 50))
            self.startTimer = True

    def towerActions(self, screen, mousePos, game, pressed):
        if util.pressedImage(mousePos, self.hitbox):
            # when the tower is pressed
            print("pressed the tower")
            self.selected()
        if self.isMenuVisible:
            if util.pressedImage(mousePos, self.upgradeRect):
                # upgrade pressed
                if pressed[0]:
                    # upgrade
                    self.upgrade(screen, game)
                    self.isMenuVisible = False

                elif pressed[2]:
                    # info about upgrade
                    self.label = myfont.render(f"cost: {self.getPrice(self.type)}", False, (51, 255, 51))
                    screen.blit(self.label, (300, 50))
                    self.startTimer = True
                    if self.maxUpgraded:
                        self.label = myfont.render("Your tower is fully upgraded", False, (255, 51, 51))
                        screen.blit(self.label, (300, 50))
                        self.startTimer = True

            elif util.pressedImage(mousePos, self.sellRect):
                # sell is pressed
                if pressed[0]:
                    game.score.score += self.getPrice(self.type)
                    game.towerList.remove(self)
                    self.isMenuVisible = False
                elif pressed[2]:
                    self.label = myfont.render(f"score: {self.getPrice(self.type) + game.score.score}", False, (51, 255, 51))
                    screen.blit(self.label, (300, 50))
                    self.startTimer = True

    def getAnimationImages(self):
        if self.type == 1:
            return tower1
        elif self.type == 1.1:
            return tower11
        elif self.type == 2:
            return tower2
        elif self.type == 2.1:
            return tower21
        else:
            return False

    def getPrice(self, type):
        switch = {
            1: 50,
            1.1: 80,
            2: 80,
            2.1: 120
        }
        return switch.get(type)

    def getDamage(self, type):
        switch = {
            1: 75,
            1.1: 150,
            2: 150,
            2.1: 250
        }
        return switch.get(type)


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
