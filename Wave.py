import Enemy
import Position
import pygame


pygame.init()

myfont = pygame.font.Font('images/font.ttf', 50)

class Wave:
    def __init__(self, path):
        self.enemyPerWave = (3, 5, 10, 18, 25, 32, 50)
        self.enemyList = []
        self.prev_pos = Position.Position(0, 0)
        self.wave = -1
        self.isDone = False
        self.path = path
        self.passedTime = 0

    def draw(self, screen, game, diff_time):
        for enemy in self.enemyList:
            if enemy.isDead and enemy.checkIsDead:
                game.score.score += 5
                enemy.checkIsDead = False
            enemy.update(screen, diff_time)
            game.enemies.add(enemy)

        waveLabel = myfont.render(f"Wave: {self.wave + 1}", 1, (169, 186, 203))
        screen.blit(waveLabel, (900, 75))
        if self.wave < len(self.enemyPerWave):
            self.create()



    def nextWave(self):
        self.wave += 1
        for enemy in self.enemyList:
            enemy.kill()
        self.enemyList = []
        if self.wave >= len(self.enemyPerWave):
            self.isDone = True
            print("The game is done!")

        if self.wave < len(self.enemyPerWave) and not self.isDone:
            self.create()


    def create(self):
        if not self.enemyList or self.enemyList[-1].position.overPos(self.path.get_pos(0.75)) and len(self.enemyList) < self.enemyPerWave[self.wave]:
            #print("Creating new enemy...")
            self.enemyList.append(Enemy.Enemy(0, 420))

    def allDead(self):
        if self.wave < len(self.enemyPerWave):
            if self.enemyList[-1].isDead and len(self.enemyList) == self.enemyPerWave[self.wave]:
                return True


if __name__ == '__main__':
    wave = Wave()
    wave.nextWave()