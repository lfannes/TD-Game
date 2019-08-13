import pygame
import Game
pygame.init()

screenWidth = 1200+300
screenHeight = 800

#globals(screenWidth, screenHeight)

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('TD Game')

def drawGame(diff_time):
    game.draw(screen, diff_time)

game = Game.Game()
clock = pygame.time.Clock()

prev_ms = pygame.time.get_ticks()


run = True
while run:
    clock.tick(60)

    while not game.isSetupDone:
        now_ms = pygame.time.get_ticks()
        diff_ms = now_ms - prev_ms
        diff_s = diff_ms / 1000

        game.setup(screen, diff_s)

        prev_ms = now_ms

    now_ms = pygame.time.get_ticks()
    diff_ms = now_ms - prev_ms
    diff_s = diff_ms / 1000

    drawGame(diff_s)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            game.mouseEvent(screen, mousePos, pygame.mouse.get_pressed())

    prev_ms = now_ms
average = 0
for number in game.avg:
    average += number
average = average/len(game.avg)
print(f"average: {average*1000}")
pygame.quit()

