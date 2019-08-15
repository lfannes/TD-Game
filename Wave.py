import Enemy
import Position
import pygame
import random

pygame.init()

myfont = pygame.font.Font('images/font.ttf', 50)

class EnemyFactory:
    def __init__(self):
        pass

    def create(self, type):
        enemy = Enemy.Enemy(type)
        return enemy

class Wave:
    def __init__(self, path):
        self.waves = [
            [1, 1, 1],
            [1, 1, 2, 2, 1, 1],
            [1, 1, 1, 2, 2, 1, 2, 3, 2, 1, 3, 2],
            [1, 1, 2, 2, 3, 4, 1, 2, 2, 4, 1, 2, 2, 3],
            [1, 1, 2, 3, 3, 2, 1, 2, 3, 4, 4, 2, 3, 4, 1, 3, 4]
        ]
        self.enemy1PerWave = (3, 5, 10, 15, 15, 15, 15)
        self.enemy2PerWave = (0, 1, 3, 5, 7, 12, 20)
        self.enemy3PerWave = (0, 0, 1, 3, 5, 7, 12)
        self.enemy4PerWave = (0, 0, 0, 1, 3, 5, 7)
        self.enemyList = []
        self.prev_pos = Position.Position(0, 0)
        self.wave = -1
        self.isDone = False
        self.path = path
        self.passedTime = 0
        self.enemyCount = 0
        self.enemyFactory = EnemyFactory()
        self.timeForNextEnemy = 0.75
        self.extraHealth = 0

    def draw(self, screen, game, diff_time):
        for enemy in self.enemyList:
            if enemy.isDead and enemy.checkIsDead:
                game.score.score += enemy.score
                enemy.checkIsDead = False
            enemy.update(screen, diff_time)
            game.enemies.add(enemy)

        waveLabel = myfont.render(f"Wave: {self.wave + 1}", 1, (169, 186, 203))
        screen.blit(waveLabel, (900, 75))
        if not self.isDone:
            self.createEnemy()



    def nextWave(self):
        self.extraHealth = self.wave*5
        self.wave += 1
        for enemy in self.enemyList:
            enemy.kill()
        self.enemyList = []
        self.enemyCount = 0
        self.timeForNextEnemy *= 0.95
        newWave = list()

        if self.wave >= len(self.waves):
            for enemy in range(0, len(self.waves[self.wave - 1]) + 5):
                enemy = random.randint(1, 4)
                newWave.append(enemy)
            self.waves.append(newWave)



        if self.wave < len(self.waves) and not self.isDone:
            self.createEnemy()


    def createEnemy(self):
        moreEnemiesAreNeeded = len(self.enemyList) < len(self.waves[self.wave])
        isItTimeToCreateNextEnemy = self.enemyList[-1].position.overPos(self.path.get_pos(self.timeForNextEnemy)) if self.enemyList else True
        if moreEnemiesAreNeeded and isItTimeToCreateNextEnemy:
            enemy = self.enemyFactory.create(self.waves[self.wave][self.enemyCount])
            enemy.position = Position.Position(0, 420)
            enemy.health += self.extraHealth
            self.enemyList.append(enemy)
            self.enemyCount += 1


    def allDead(self):
        if self.wave < len(self.waves[self.wave]):
            if self.enemyList[-1].isDead and len(self.enemyList) == len(self.waves[self.wave]):
                return True


if __name__ == '__main__':
    wave = Wave()
    wave.nextWave()