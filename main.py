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

run = True
while run:
    for event in pygame.event.get():

        drawGame()

        if event.type == pygame.QUIT:
            run = False

pygame.quit()

