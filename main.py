import pygame
import Game

pygame.init()

screenWidth = 1200
screenHeight = 800

#globals(screenWidth, screenHeight)

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('TD Game')

def drawGame():
    game.draw(screen)

game = Game.Game()
clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)

    drawGame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()

