import pygame
import random
class Pipe:
    def __init__(self,x):
        self.image = pygame.image.load('Pipes.png')
        self.image = pygame.transform.scale(self.img, [100,100])
        self.image = self.image.get_rect()
        self.movement = 5
        self.image.rect.y = random.randint(0, 600)
        self.image.rect.x = x


    def update(self,screen):
        screen.blit(self.image,self.image.rect)        

        