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
alphaTowerImage = Towers.towerImage.set_alpha(180)


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

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
        self.avg = list()



    def draw(self, screen, diff_time):
        if not self.wave.isDone:
            self.time += diff_time
            print(diff_time)
            self.avg.append(diff_time)
            self.map.draw(screen)
            self.allSprites.update(screen, self.wave.enemyList, self.time)
            self.wave.draw(screen, self)
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

    def setup(self, screen, diff_time):
        if not self.isSetupDone:
            self.setupTime += diff_time
            pos = pygame.mouse.get_pos()
            collision = self.area.isClear(self.tower, self.unmovable)
            self.map.draw(screen)
            #blit_alpha(screen, Towers.towerImage, (pos[0] - 52, pos[1] - 81.5), 180)
            self.tower.position = Position.Position(pos[0] - 52, pos[1] - 81.5)
            self.tower.draw(screen)
            self.area.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    towerPos = pygame.mouse.get_pos()
                    if collision:
                        self.movable.remove(self.tower)
                        self.unmovable.add(self.tower)
                        print(f"towerPos: {towerPos}")
                        self.tower.position = Position.Position(pos[0] - 52, pos[1] - 81.5)
                        self.tower.draw(screen)
                        self.isSetupDone = True
                        self.time = self.setupTime
                    else:
                        print(f"unable to place the tower on {towerPos}")

            pygame.display.flip()
        else:
            return True
