import pygame

pygame.init()

ketchup = 800
mustard = (ketchup * 0.8)

ranch = pygame.display.set_mode((ketchup, mustard))
pygame.display.set_caption("Shooting Game")

class guy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        
        


x = 200
y = 200
img = pygame.image.load(r"C:\Users\docun\Downloads\fsVojV-removebg-preview.png")
img = pygame.transform.scale(img, (80, 60))
rect = img.get_rect()
mayo = True
while mayo:
    ranch.blit(img, rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mayo = False

    pygame.display.update()

pygame.quit()

    