import pygame
import Map
import Towers
import Enemy
import Path
import Position
import numpy


'''enemy = Enemy.Enemy(5, 420)
enemyList = (Enemy.Enemy(5, 420), Enemy.Enemy(180, 420))
path = Path.Path()
#path in init
pathPos = Position.Position(0, 420)
path.add(pathPos, 0)
pathPos = Position.Position(180, 420)
path.add(pathPos, 0.3)'''

class Game:
    def __init__(self):
        self.time = 0
        self.step = 0.003
        self.path = Path.Path()
        pos = Position.Position(0, 0)
        pos.y = 420; self.path.add(pos, 0)
        pos.x = 180; self.path.add(pos, 1)
        pos.y = 180; self.path.add(pos, 1)
        pos.x = 420; self.path.add(pos, 1)
        pos.y = 500; self.path.add(pos, 1)
        pos.x = 750; self.path.add(pos, 1)
        pos.y = 320; self.path.add(pos, 1)
        pos.x = 1200; self.path.add(pos, 1)

        self.enemy = Enemy.Enemy(5, 420)
        self.map = Map.Map()
        self.tower = Towers.Tower(50, 210)


    def draw(self, screen, diff_time):
        self.time += diff_time

        self.map.draw(screen)
        self.tower.draw(screen)

        newEnemyPos = self.path.get_pos(self.time)
        if newEnemyPos:
            self.enemy.move(newEnemyPos)
            self.enemy.draw(screen)

        pygame.display.update()