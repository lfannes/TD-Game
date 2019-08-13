import pygame
import Map
import Towers
import Path
import Position
import Wave
import Score
import Area
import Shop

towerDefense = pygame.image.load('images/tower-defense.png')
victory = pygame.image.load('images/victory.png')
defeat = pygame.image.load('images/defeat.png')
my_font = pygame.font.Font('images/font.ttf', 50)
lb1 = my_font.render("Can't place the tower there!!", False, (255, 51, 51))


class Game:
    def __init__(self):
        self.time = 0
        self.step = 0.003
        self.path = Path.Path()
        pos = Position.Position(0, 0)
        pos.y = 420; self.path.add(pos, 0)
        pos.x = 90; self.path.add(pos, 1)
        pos.x = 180; self.path.add(pos, 1)
        pos.y = 180; self.path.add(pos, 2)
        pos.x = 420; self.path.add(pos, 2)
        pos.y = 500; self.path.add(pos, 2)
        pos.x = 750; self.path.add(pos, 2)
        pos.y = 330; self.path.add(pos, 1)
        pos.x = 1250; self.path.add(pos, 2)
        pos.x = 1350; self.path.add(pos, 2)
        self.tower = Towers.Tower(0, 0)
        self.map = Map.Map()
        self.area = Area.Area()
        self.wave = Wave.Wave(self.path)
        self.wave.nextWave()
        self.score = Score.Score()
        self.shop = Shop.Shop()
        self.isSetupDone = False
        self.setupTime = 0
        self.newTower = False
        self.newTowerType = 0
        self.enemies = pygame.sprite.Group()
        self.towerList = list()
        self.avg = list()
        self.timer = 0
        self.startTimer = False



    def draw(self, screen, diff_time):
        if not self.wave.isDone:
            self.time += diff_time
            self.avg.append(diff_time)
            screen.fill((47, 79, 79))
            self.map.draw(screen)
            self.shop.draw(screen, diff_time, self)
            for tower in self.towerList:
                tower.update(screen, self.wave.enemyList, self.time, diff_time)
            self.enemies.update(screen, diff_time)
            self.wave.draw(screen, self, diff_time)
            self.score.draw(screen)
            self.score.hit(self.path, self.wave.enemyList)

            for enemy in self.wave.enemyList:
                enemy.time += diff_time
                newEnemyPos = self.path.get_pos(enemy.time)
                if newEnemyPos:
                    enemy.move(newEnemyPos)

            lastEnemyPos = True
            if self.wave.wave < len(self.wave.enemy1PerWave):
                lastEnemyPos = self.path.get_pos(self.wave.enemyList[-1].time)
            if not lastEnemyPos or self.wave.allDead():
                self.wave.nextWave()

            if self.score.isDead:
                screen.fill((47, 79, 79))
                screen.blit(towerDefense, (450, 75))
                screen.blit(defeat, (350, 370))

            if self.newTower:
                self.placeNewTower(screen, diff_time)

        if self.wave.isDone and not self.score.isDead:
            screen.fill((47,79,79))
            screen.blit(towerDefense, (450, 75))
            screen.blit(victory, (300, 320))

        pygame.display.update()

    def mouseEvent(self, screen, mousePos, pressed):
        print("mouseEvent")
        for tower in self.towerList:
            tower.towerActions(screen, mousePos, self, pressed)
        self.shop.shopActions(screen, mousePos, self)

    def setup(self, screen, diff_time):
        if not self.isSetupDone:
            self.setupTime += diff_time
            pos = pygame.mouse.get_pos()
            screen.fill((47, 79, 79))
            self.shop.draw(screen, None, self)
            self.map.draw(screen)
            collision = self.area.isClear(self.tower, self.area, self.map, None)
            print(f"col: {collision}")
            self.tower.placing(screen, 200, (pos[0] - 50, pos[1] - 50), collision, 1)

            if self.startTimer:
                screen.blit(lb1, (300, 50))
                self.timer += diff_time
                print(self.timer)
                if self.timer >= 2.5:
                    self.startTimer = False
                    self.timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    towerPos = pygame.mouse.get_pos()
                    if collision:
                        self.tower.place(towerPos)
                        self.tower.draw(screen, diff_time)
                        self.towerList.append(self.tower)
                        self.isSetupDone = True
                        self.time = self.setupTime
                        self.tower = Towers.Tower(0, 0)
                    else:
                        print(f"unable to place the tower on {towerPos}")

                        screen.blit(lb1, (300, 50))
                        self.startTimer = True


            pygame.display.flip()
        else:
            return True

    def placeNewTower(self, screen, diff_time):
        pos = pygame.mouse.get_pos()

        collisionList = list()
        for item in self.towerList:
            collision = self.area.isClear(self.tower, self.area, self.map, item)
            collisionList.append(collision)

        collision = True
        for item in collisionList:
            if item == False:
                collision = False

        self.tower.placing(screen, 200, (pos[0] - 50, pos[1] - 50), collision, self.newTowerType)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                towerPos = pygame.mouse.get_pos()
                if collision:
                    self.tower.place(towerPos)
                    self.tower.draw(screen, diff_time)
                    self.towerList.append(self.tower)
                    self.newTower = False
                    self.tower = Towers.Tower(0, 0)
            elif event.type == pygame.K_ESCAPE:
                self.newTower = False
                break