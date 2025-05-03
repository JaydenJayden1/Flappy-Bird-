import pygame
import random

class Pipe:
    def __init__(self,x):
        self.image = pygame.image.load('Pipes.png')
        self.image = pygame.transform.scale(self.image, [400,600])
        self.rect = self.image.get_rect()
        self.movement = 5
        self.rect.y= random.randint(400, 450)
        self.rect.x = x
    
    

    def update(self,screen): 
        if self.rect.x <= -400:
            self.rect.x = 700
            self.rect.y= random.randint(400, 450)
        screen.blit(self.image,self.rect)  
        self.rect.x -= self.movement
         

        