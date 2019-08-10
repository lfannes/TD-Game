import Enemy
import Position
import pygame


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
            [1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 3, 1, 1, 1, 2],
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

    def draw(self, screen, game, diff_time):
        for enemy in self.enemyList:
            if enemy.isDead and enemy.checkIsDead:
                game.score.score += 5
                enemy.checkIsDead = False
            enemy.update(screen, diff_time)
            game.enemies.add(enemy)

        waveLabel = myfont.render(f"Wave: {self.wave + 1}", 1, (169, 186, 203))
        screen.blit(waveLabel, (900, 75))
        if not self.isDone:
            self.createEnemy()



    def nextWave(self):
        self.wave += 1
        for enemy in self.enemyList:
            enemy.kill()
        self.enemyList = []
        self.enemyCount = 0

        if self.wave >= len(self.enemy1PerWave):
            self.isDone = True
            print("The game is done!")

        if self.wave < len(self.enemy1PerWave) and not self.isDone:
            self.createEnemy()


    def createEnemy(self):
        moreEnemiesAreNeeded = len(self.enemyList) < len(self.waves[self.wave])
        isItTimeToCreateNextEnemy = self.enemyList[-1].position.overPos(self.path.get_pos(0.75)) if self.enemyList else True
        if moreEnemiesAreNeeded and isItTimeToCreateNextEnemy:
            enemy = self.enemyFactory.create(self.waves[self.wave][self.enemyCount])
            enemy.position = Position.Position(0, 420)
            self.enemyList.append(enemy)
            self.enemyCount += 1


    def allDead(self):
        if self.wave < len(self.enemy1PerWave):
            if self.enemyList[-1].isDead and len(self.enemyList) == self.enemy1PerWave[self.wave]:
                return True


if __name__ == '__main__':
    wave = Wave()
    wave.nextWave()