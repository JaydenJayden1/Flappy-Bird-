import pygame
from pipe import Pipe
# This is the main file that runs the game
# and manages the game loop
pygame.init()
background=pygame.display.set_mode((400,600))
clock= pygame.time.Clock()
player = pygame.image.load('Flappy bird.png').convert_alpha()
player = pygame.transform.smoothscale(player, (100,100))
player = player.subsurface(player.get_bounding_rect().inflate(-0, -0)) #inflate(x,y) changes the size of bounding box by x and y pixels
pygame.image.save(player, "player.png")
print(player.get_height())
print(player.get_width())
player_pos = player.get_rect(topleft = [20,240])
why_speed = 0
pipe = pygame.image.load('Pipes.png')
#print("height:" + player.get_bounding_rect().height)
#print("width:" + player.get_bounding_rect().width)

pipe1 = Pipe(50)

## Set the initial position of the player
game_running = True
font = pygame.font.SysFont("impact", 30)
while game_running:
    
    jump=False
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_running=False
            pygame.quit() 
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE or event.key==pygame.K_UP:
                jump=True
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                jump=True

 
    # Update the position of the pipe
    background.fill("sky blue")
    pipe1.update(background,player_pos)
    why_speed+=.26
    if jump:
        why_speed=-5
    player_pos.y+=why_speed
    if not background.get_rect().contains(player_pos):
        quit()
    background.blit(player,player_pos)
    text = font.render(f"Your Score [{Pipe.score}]", True, "black")
    background.blit(text,[0,0])
    pygame.display. flip()
    clock.tick(60) 
