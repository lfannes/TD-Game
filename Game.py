import pygame
import Map
import Towers
import Path
import Position
import Wave

towerDefense = pygame.image.load('images/tower-defense.png')
victory = pygame.image.load('images/victory.png')

class Game:
    def __init__(self):
        self.time = 0
        self.step = 0.003
        self.path = Path.Path()
        pos = Position.Position(0, 0)
        pos.y = 420; self.path.add(pos, 0)
        pos.x = 90; self.path.add(pos, 0.5)
        pos.x = 180; self.path.add(pos, 0.5)
        pos.y = 180; self.path.add(pos, 1)
        pos.x = 420; self.path.add(pos, 1)
        pos.y = 500; self.path.add(pos, 1)
        pos.x = 750; self.path.add(pos, 1)
        pos.y = 330; self.path.add(pos, 0.5)
        pos.x = 1250; self.path.add(pos, 1)
        self.enemyList = list()
        self.map = Map.Map()
        self.tower = Towers.Tower(50, 210)
        self.wave = Wave.Wave()
        self.wave.nextWave()



    def draw(self, screen, diff_time):
        if not self.wave.isDone:
            self.time += diff_time

            self.map.draw(screen)
            self.tower.draw(screen)
            self.wave.draw(screen, 0.5, self.path)


            for enemy in self.wave.enemyList:
                enemy.time += diff_time
                newEnemyPos = self.path.get_pos(enemy.time)
                if newEnemyPos:
                    enemy.move(newEnemyPos)

            lastEnemyPos = self.path.get_pos(self.wave.enemyList[-1].time)
            if not lastEnemyPos:
                self.wave.nextWave()
        else:
            screen.fill((47,79,79))
            screen.blit(towerDefense, (450, 75))
            screen.blit(victory, (300, 320))

        pygame.display.update()
