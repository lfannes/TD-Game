import pygame
import Map
import Towers
import Enemy

map = Map.Map()
tower = Towers.Tower(50, 210)
enemyList = (Enemy.Enemy(5, 420), Enemy.Enemy(180, 420))


class Game:
    def __init__(self):
        pass

    def draw(self, screen):
        map.draw(screen)
        tower.draw(screen)
        for enemy in enemyList:
            enemy.draw(screen)
        #print("DRAW")
        pygame.display.update()
