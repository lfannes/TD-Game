import Enemy
import Position
import pygame

pygame.init()

myfont = pygame.font.Font('images/BAUHS93.TTF', 50)

class Wave:
    def __init__(self, path):
        self.enemyPerWave = (5, 6, 10)
        self.enemyList = []
        self.prev_pos = Position.Position(0, 0)
        self.wave = -1
        self.isDone = False
        self.path = path

    def draw(self, screen, time, path):
        for enemy in self.enemyList:
            enemy.draw(screen)
        waveLabel = myfont.render(f"Wave: {self.wave + 1}", 1, (119,136,153))
        screen.blit(waveLabel, (900, 75))
        if self.wave < len(self.enemyPerWave):
            self.create()



    def nextWave(self):
        self.wave += 1
        self.enemyList = []
        if self.wave >= len(self.enemyPerWave):
            self.isDone = True
            print("The game is done!")

        if self.wave < len(self.enemyPerWave) and not self.isDone:
            self.create()


    def create(self):
        if not self.enemyList or self.enemyList[-1].position.overPos(self.path.get_pos(0.5)) and len(self.enemyList) < self.enemyPerWave[self.wave]:
            #print("Creating new enemy...")
            self.enemyList.append(Enemy.Enemy(0, 420))

    def allDead(self):
        if self.wave < len(self.enemyPerWave):
            if self.enemyList[-1].isDead and len(self.enemyList) == self.enemyPerWave[self.wave]:
                print("True111")
                return True


if __name__ == '__main__':
    wave = Wave()
    wave.nextWave()