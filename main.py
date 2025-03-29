import pygame
pygame.init()
background=pygame.display.set_mode((400,600))
background.fill("blue")

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            pygame.quit()
    pygame.display.flip()