import pygame
import Map
import Towers
import Enemy
import Path
import Position
import numpy

map = Map.Map()
tower = Towers.Tower(50, 210)
enemy = Enemy.Enemy(5, 420)
enemyList = (Enemy.Enemy(5, 420), Enemy.Enemy(180, 420))
path = Path.Path()

pathPos = Position.Position(0, 420)
path.add(pathPos, 0)
pathPos = Position.Position(180, 420)
path.add(pathPos, 0.3)

class Game:
    def __init__(self):
        self.time = 0
        self.step = 0.003


    def draw(self, screen):
        map.draw(screen)
        tower.draw(screen)
        for enemy_ in enemyList:
            enemy_.draw(screen)
        enemy.draw(screen)

        if self.time <= path.max_time():
            print(enemy.get_vel(path, self.step))
            enemy.move(enemy.get_vel(path, self.step))
            enemy.draw(screen)
            self.time += self.step
            #print(self.time)

        pygame.display.update()