import Enemy
import Position
import pygame

pygame.init()

myfont = pygame.font.Font('images/BAUHS93.TTF', 50)

class Wave:
    def __init__(self):
        self.enemyPerWave = (3, 5, 8, 12, 18, 25, 32     )
        self.enemyList = []
        self.prev_pos = Position.Position(0, 0)
        self.wave = -1
        self.isDone = False

    def draw(self, screen, time, path):
        for enemy in self.enemyList:
            enemy.draw(screen)
        waveLabel = myfont.render(f"Wave: {self.wave + 1}", 1, (119,136,153))
        screen.blit(waveLabel, (900, 75))
        self.create(time, path)



    def nextWave(self):
        self.wave += 1
        self.enemyList = []
        if not self.isDone:
            print("Creating new enemy...")
            self.enemyList.append(Enemy.Enemy(0, 420))


    def create(self, time, path):
        try:
            if self.enemyList[-1].position.overPos(path.get_pos(time)) and len(self.enemyList) < self.enemyPerWave[self.wave]:
                #print("Creating new enemy...")
                self.enemyList.append(Enemy.Enemy(0, 420))
        except IndexError:
            self.isDone = True
            print("The game is done!")


if __name__ == '__main__':
    wave = Wave()
    wave.nextWave()