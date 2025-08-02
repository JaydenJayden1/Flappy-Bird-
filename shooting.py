import pygame

pygame.init()

ketchup = 800
mustard = (ketchup * 0.8)

ranch = pygame.display.set_mode((ketchup, mustard))
pygame.display.set_caption("Shooting Game")

class guy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(r"C:\Users\docun\Downloads\fsVojV-removebg-preview.png")
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int (img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center * (x,y)    
        
        
player = guy(200, 200, 3)



mayo = True
while mayo:
    ranch.blit(player.image, player.rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mayo = False

    pygame.display.update()

pygame.quit()

    