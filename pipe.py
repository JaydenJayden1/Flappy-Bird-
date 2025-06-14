import pygame
import random
# This class is used to create the pipe object
# and manage its position and movement
class Pipe:
    score = 0
    def __init__(self,x):
        self.image = pygame.image.load('Pipes.png')
        self.image = pygame.transform.scale(self.image, [400,600])
        self.image2 = pygame.transform.flip(self.image, False, True)
        self.image = self.image.subsurface(self.image.get_bounding_rect().inflate(-0, -0))
        self.image2 = self.image2.subsurface(self.image2.get_bounding_rect().inflate(-0, -0))
        pygame.image.save(self.image, "pipe2.png")
        pygame.image.save(self.image2, "pipe.png")
        self.rect2 = self.image2.get_rect()
        self.rect = self.image.get_rect()
        self.movement = 5
        self.rect.y= random.randint(400, 450)
        self.rect.x = x
        self.rect2.x = self.rect.x
        self.rect2.y = self.rect.y - 750
    
     #U#and draw it on the screen
    def collision(self, bird):
        if bird.colliderect(self.rect) or bird.colliderect(self.rect2):
           pygame.quit()

         

    def update(self,screen,bird): 
        self.collision(bird)
        if self.rect.right <= 0:
            self.rect.x = 700
            self.rect.y= random.randint(400, 450)
            self.rect2.x = 700
            self.rect2.y= self.rect.y - 750
            Pipe.score += 1

        screen.blit(self.image,self.rect)  
        screen.blit(self.image2,self.rect2)
        self.rect.x -= self.movement
        self.rect2.x -= self.movement

