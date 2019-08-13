import util
import pygame

tower1 = pygame.image.load('images/tower21.png')
tower1 = util.scaleSingleImage(tower1, 2)

tower11 = pygame.image.load('images/tower23.png')
tower11 = util.scaleSingleImage(tower11, 2)

tower2 = pygame.image.load('images/tower30.png')
tower2 = util.scaleSingleImage(tower2, 2)

tower21 = pygame.image.load('images/tower31.png')
tower21 = util.scaleSingleImage(tower21, 2)

myfont = pygame.font.Font('images/font.TTF', 50)
priceFont = pygame.font.Font('images/Dollar.ttf', 50)

class TowerStruct:
    def __init__(self, pos, type, ):
        self.type = type
        self.image = self.getImage()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.label = None
        self.startTimer = False
        self.timer = 0

    def getImage(self):
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

    def draw(self, screen, diff_time):
        screen.blit(self.image, self.rect.topleft)

        if self.startTimer:
            screen.blit(self.label, (300, 50))
            self.timer += diff_time
            if self.timer >= 2.5:
                self.startTimer = False
                self.timer = 0


    def pressed(self, game):
        print(f"pressed a type: {self.type} tower")
        if game.score.score >= game.tower.getPrice(self.type):
            print("buy")
            game.newTower = True
            game.newTowerType = self.type
            game.score.score -= game.tower.getPrice(self.type)
        else:
            self.label = myfont.render("You don't have enough money!", False, (255, 51, 51))
            self.startTimer = True



class Shop:
    def __init__(self):
        self.allItems = list()
        self.towerItem1 = TowerStruct((1300, 50), 1)
        self.towerItem2 = TowerStruct((1300, 400), 2)
        self.allItems.append(self.towerItem1)
        self.allItems.append(self.towerItem2)

    def draw(self, screen, diff_time, game):
        for item in self.allItems:
            item.draw(screen, diff_time)
            priceLabel = priceFont.render(f"${game.tower.getPrice(item.type)}", False, (0, 255, 0))
            screen.blit(priceLabel, (item.rect.x, item.rect.y + item.image.get_height()))

    def shopActions(self, screen, mousePos, game):
        for item in self.allItems:
            if util.pressedImage(mousePos, item.rect):
                    item.pressed(game)