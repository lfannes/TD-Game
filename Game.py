import pygame
import Map
import Towers
import Path
import Position
import Wave
import Score
import Area

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
        self.isSetupDone = False
        self.setupTime = 0

        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.area, self.tower)
        self.unmovable = pygame.sprite.Group()
        self.unmovable.add(self.area)
        self.movable = pygame.sprite.Group()
        self.movable.add(self.tower)
        self.enemies = pygame.sprite.Group()
        self.avg = list()
        self.timer = 0
        self.startTimer = False



    def draw(self, screen, diff_time):
        if not self.wave.isDone:
            self.time += diff_time
            self.avg.append(diff_time)
            self.map.draw(screen)
            self.tower.update(screen, self.wave.enemyList, self.time, diff_time)
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
            if self.wave.wave < len(self.wave.enemyPerWave):
                lastEnemyPos = self.path.get_pos(self.wave.enemyList[-1].time)
            if not lastEnemyPos or self.wave.allDead():
                self.wave.nextWave()

            if self.score.isDead:
                screen.fill((47, 79, 79))
                screen.blit(towerDefense, (450, 75))
                screen.blit(defeat, (350, 370))

        if self.wave.isDone and not self.score.isDead:
            screen.fill((47,79,79))
            screen.blit(towerDefense, (450, 75))
            screen.blit(victory, (300, 320))

        pygame.display.update()

    def mouseEvent(self, screen, mousePos, pressed):
        print("mouseEvent")
        self.tower.towerActions(screen, mousePos, self, pressed)

    def setup(self, screen, diff_time):
        if not self.isSetupDone:
            self.setupTime += diff_time
            pos = pygame.mouse.get_pos()

            self.map.draw(screen)
            collision = self.area.isClear(self.tower, self.area)
            self.tower.placing(screen, 200, (pos[0] - 50, pos[1] - 50), collision)


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
                    if not collision:
                        self.movable.remove(self.tower)
                        self.unmovable.add(self.tower)
                        self.tower.place(towerPos)
                        self.tower.draw(screen, diff_time)
                        self.isSetupDone = True
                        self.time = self.setupTime
                    else:
                        print(f"unable to place the tower on {towerPos}")

                        screen.blit(lb1, (300, 50))
                        self.startTimer = True


            pygame.display.flip()
        else:
            return True
