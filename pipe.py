import pygame
import random
# This class is used to create the pipe object
# and manage its position and movement
class Pipe:
    def __init__(self,x):
        self.image = pygame.image.load('Pipes.png')
        self.image = pygame.transform.scale(self.image, [400,600])
        self.image2 = pygame.transform.flip(self.image, False, True)
        self.rect2 = self.image2.get_rect()
        self.rect = self.image.get_rect()
        self.movement = 5
        self.rect.y= random.randint(400, 450)
        self.rect.x = x
        self.rect2.x = self.rect.x
        self.rect2.y = self.rect.y - 750
    
    # Update the position of the pipe
    # and draw it on the screen

    def update(self,screen): 

        if self.rect.x <= -400:
            self.rect.x = 700
            self.rect.y= random.randint(400, 450)
            self.rect2.x = 700
            self.rect2.y= self.rect.y - 750

        screen.blit(self.image,self.rect)  
        screen.blit(self.image2,self.rect2)
        self.rect.x -= self.movement
        self.rect2.x -= self.movement
         

        