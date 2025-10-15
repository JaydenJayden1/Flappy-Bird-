import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.font
import pygame.image
import pygame.joystick
import pygame.key
import pygame.mixer
import pygame.mouse
import pygame.sprite
import pygame.surface
import pygame.time
import pygame.transform
import pygame.camera
import pygame.mask
import pygame.math
import pygame._sdl2
from pygame.locals import *
import sys 
import random
import os
import time
import math
import datetime
import json
import re
import csv
import subprocess
import threading
import logging
import shutil
import zipfile
import webbrowser
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Halloween Game")
clock = pygame.time.Clock()
running = True
paused = False
game_started = False
game_over = False
you_win = False
# ---Start of the images for slides---
slide_image1 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (1).png").convert_alpha()
slide_image1 = pygame.transform.scale(slide_image1, (200,200))

slide_image2 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (2).png").convert_alpha()
slide_image2 = pygame.transform.scale(slide_image2, (200,200))

slide_image3 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (3).png").convert_alpha()
slide_image3 = pygame.transform.scale(slide_image3, (200,200))

slide_image4 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (4).png").convert_alpha()
slide_image4 = pygame.transform.scale(slide_image4, (200,200))

slide_image5 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (5).png").convert_alpha()
slide_image5 = pygame.transform.scale(slide_image5, (200,200))

slide_image6 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (6).png").convert_alpha()
slide_image6 = pygame.transform.scale(slide_image6, (200,200))

slide_image7 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (7).png").convert_alpha()
slide_image7 = pygame.transform.scale(slide_image7, (200,200))

slide_image8 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (8).png").convert_alpha()
slide_image8 = pygame.transform.scale(slide_image8, (200,200))

slide_image9 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (9).png").convert_alpha()
slide_image9 = pygame.transform.scale(slide_image9, (200,200))

slide_image10 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Slide (10).png").convert_alpha()
slide_image10 = pygame.transform.scale(slide_image10, (200,200))
# ---End of the images for slides---





# ---Start of the images for deads---
dead_image1 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (1).png").convert_alpha()
dead_image1 = pygame.transform.scale(dead_image1, (200,200))

dead_image2 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (2).png").convert_alpha()
dead_image2 = pygame.transform.scale(dead_image2, (200,200))

dead_image3 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (3).png").convert_alpha()
dead_image3 = pygame.transform.scale(dead_image3, (200,200))

dead_image4 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (4).png").convert_alpha()
dead_image4 = pygame.transform.scale(dead_image4, (200,200))

dead_image5 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (5).png").convert_alpha()
dead_image5 = pygame.transform.scale(dead_image5, (200,200))

dead_image6 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (6).png").convert_alpha()
dead_image6 = pygame.transform.scale(dead_image6, (200,200))

dead_image7 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (7).png").convert_alpha()
dead_image7 = pygame.transform.scale(dead_image7, (200,200))

dead_image8 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (8).png").convert_alpha()
dead_image8 = pygame.transform.scale(dead_image8, (200,200))

dead_image9 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (9).png").convert_alpha()
dead_image9 = pygame.transform.scale(dead_image9, (200,200))

dead_image10 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Dead (10).png").convert_alpha()
dead_image10 = pygame.transform.scale(dead_image10, (200,200))
# ---End of the images for deads---





# ---Start of the images for jumps---
jump_image1 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (1).png").convert_alpha()
jump_image1 = pygame.transform.scale(jump_image1, (200,200))

jump_image2 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (2).png").convert_alpha()
jump_image2 = pygame.transform.scale(jump_image2, (200,200))

jump_image3 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (3).png").convert_alpha()
jump_image3 = pygame.transform.scale(jump_image3, (200,200))

jump_image4 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (4).png").convert_alpha()
jump_image4 = pygame.transform.scale(jump_image4, (200,200))

jump_image5 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (5).png").convert_alpha()
jump_image5 = pygame.transform.scale(jump_image5, (200,200))

jump_image6 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (6).png").convert_alpha()
jump_image6 = pygame.transform.scale(jump_image6, (200,200))

jump_image7 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (7).png").convert_alpha()
jump_image7 = pygame.transform.scale(jump_image7, (200,200))

jump_image8 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (8).png").convert_alpha()
jump_image8 = pygame.transform.scale(jump_image8, (200,200))

jump_image9 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (9).png").convert_alpha()
jump_image9 = pygame.transform.scale(jump_image9, (200,200))

jump_image10 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Jump (10).png").convert_alpha()
jump_image10 = pygame.transform.scale(jump_image10, (200,200))
# ---End of the images for jumps---





# ---Start of the images for runs---
run_image1 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (1).png").convert_alpha()
run_image1 = pygame.transform.scale(run_image1, (200,200))

run_image2 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (2).png").convert_alpha()
run_image2 = pygame.transform.scale(run_image2, (200,200))

run_image3 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (3).png").convert_alpha()
run_image3 = pygame.transform.scale(run_image3, (200,200))

run_image4 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (4).png").convert_alpha()
run_image4 = pygame.transform.scale(run_image4, (200,200))

run_image5 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (5).png").convert_alpha()
run_image5 = pygame.transform.scale(run_image5, (200,200))

run_image6 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (6).png").convert_alpha()
run_image6 = pygame.transform.scale(run_image6, (200,200))

run_image7 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (7).png").convert_alpha()
run_image7 = pygame.transform.scale(run_image7, (200,200))

run_image8 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Run (8).png").convert_alpha()
run_image8 = pygame.transform.scale(run_image8, (200,200))
# ---End of the images for runs---





# ---Start of the images for walks---
walk_image1 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (1).png").convert_alpha()
walk_image1 = pygame.transform.scale(walk_image1, (200,200))

walk_image2 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (2).png").convert_alpha()
walk_image2 = pygame.transform.scale(walk_image2, (200,200))

walk_image3 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (3).png").convert_alpha()
walk_image3 = pygame.transform.scale(walk_image3, (200,200))

walk_image4 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (4).png").convert_alpha()
walk_image4 = pygame.transform.scale(walk_image4, (200,200))

walk_image5 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (5).png").convert_alpha()
walk_image5 = pygame.transform.scale(walk_image5, (200,200))

walk_image6 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (6).png").convert_alpha()
walk_image6 = pygame.transform.scale(walk_image6, (200,200))

walk_image7 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (7).png").convert_alpha()
walk_image7 = pygame.transform.scale(walk_image7, (200,200))

walk_image8 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (8).png").convert_alpha()
walk_image8 = pygame.transform.scale(walk_image8, (200,200))

walk_image9 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (9).png").convert_alpha()
walk_image9 = pygame.transform.scale(walk_image9, (200,200))

walk_image10 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Walk (10).png").convert_alpha()
walk_image10 = pygame.transform.scale(walk_image10, (200,200))
# ---End of the images for walks---





# ---Start of the images for idles---
idle_image1 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (1).png").convert_alpha()
idle_image1 = pygame.transform.scale(idle_image1, (200,200))

idle_image2 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (2).png").convert_alpha()
idle_image2 = pygame.transform.scale(idle_image2, (200,200))

idle_image3 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (3).png").convert_alpha()
idle_image3 = pygame.transform.scale(idle_image3, (200,200))

idle_image4 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (4).png").convert_alpha()
idle_image4 = pygame.transform.scale(idle_image4, (200,200))

idle_image5 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (5).png").convert_alpha()
idle_image5 = pygame.transform.scale(idle_image5, (200,200))

idle_image6 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (6).png").convert_alpha()
idle_image6 = pygame.transform.scale(idle_image6, (200,200))

idle_image7 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (7).png").convert_alpha()
idle_image7 = pygame.transform.scale(idle_image7, (200,200))

idle_image8 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (8).png").convert_alpha()
idle_image8 = pygame.transform.scale(idle_image8, (200,200))

idle_image9 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (9).png").convert_alpha()
idle_image9 = pygame.transform.scale(idle_image9, (200,200))

idle_image10 = pygame.image.load("C:/Users/docun/Downloads/jackfree/png/Idle (10).png").convert_alpha()
idle_image10 = pygame.transform.scale(idle_image10, (200,200))
# ---End of the images for idles---

#FINISHED ALL THE IMAGES FOR JACKFREE!
#BUTT STILL NEED TO ADD BACKGROUND, OBSTACLES, AND OTHER STUFF LIKE XMAS MAN
#also in this process i learned how to put a image with the C:/Users whatever thing instead of the other way. I think this works of better and is much less confusing for me
