# Example file showing a basic pygame "game loop"
#
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image,[1920,1080])
background_rect = background_image.get_rect()




player = pygame.Vector2(1920, 1080)/2
angle = 180
speed = pygame.Vector2()
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
    angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
    speed *= .75
    player += speed.rotate(angle)
    screen.blit(background_image, background_rect)
    # fill the screen with a color to wipe away anything from last frame
    pygame.draw.circle(screen, "white", player, 20)
    pygame.draw.line(screen , "red" , player , player + pygame.Vector2(21, 0).rotate(angle))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()