import pygame
import Map
import Towers
import Path
import Position
import Wave
import Score

towerDefense = pygame.image.load('images/tower-defense.png')
victory = pygame.image.load('images/victory.png')
defeat = pygame.image.load('images/defeat.png')

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
        self.wave = Wave.Wave(self.path)
        self.wave.nextWave()
        self.score = Score.Score()
        self.isSetupDone = False
        self.setupTime = 0



    def draw(self, screen, diff_time):
        if not self.wave.isDone:
            self.time += diff_time

            self.map.draw(screen)
            self.tower.draw(screen)
            self.tower.shoot(self.wave.enemyList, self.time)
            self.wave.draw(screen, 0.5, self.path)
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

            self.map.draw(screen)
            self.tower.position = Position.Position(pos[0] - 52, pos[1] - 81.5)
            self.tower.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    towerPos = pygame.mouse.get_pos()
                    print(f"towerPos: {towerPos}")
                    self.tower.position = Position.Position(pos[0] - 52, pos[1] - 81.5)
                    self.tower.draw(screen)
                    self.isSetupDone = True
                    self.time = self.setupTime

            pygame.display.update()
        else:
            return True