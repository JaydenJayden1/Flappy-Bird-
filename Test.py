import pygame
import random
import sys
import time

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Game states
waiting_to_start = True
paused = False
second_win = False

# Pause timing
pause_start_time = 0
total_paused_time = 0

# Load and play background music
pygame.mixer.music.load('Not Like Us.mp3')
pygame.mixer.music.set_volume(0.6)

# Load images
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

explosion = pygame.image.load('cartoon-type-explosion-drawing-red-orange-yellow-violent-110908926-removebg-preview.png')
explosion = pygame.transform.scale(explosion, (60, 60))

base_astroid_img = pygame.image.load('Astriod-removebg-preview.png')
base_astroid_img = pygame.transform.scale(base_astroid_img, (60, 60))

Game_Winner = pygame.image.load('OIP__11_-removebg-preview.png')
Second_Winner = pygame.image.load('ast-uranus-removebg-preview.png')

ufo_img = pygame.image.load('ufo-cartoon-alien-spaceship-cosmic-ship-form-saucer-ufo-cartoon-alien-spaceship-cosmic-ship-form-saucer-181588751-removebg-preview.png')
ufo_img = pygame.transform.scale(ufo_img, (80, 50))

# Load sounds
death_sound = pygame.mixer.Sound('mixkit-explosion-hit-1704.wav')
death_sound.set_volume(0.7)
laser_sound = pygame.mixer.Sound('mixkit-short-laser-gun-shot-1670.wav')
laser_sound.set_volume(0.5)
# UFO laser sound (optional)
try:
    ufo_laser_sound = pygame.mixer.Sound('ufo-laser.wav')
    ufo_laser_sound.set_volume(0.5)
except FileNotFoundError:
    ufo_laser_sound = None

# Fonts
font = pygame.font.SysFont(None, 50)
big_font = pygame.font.SysFont(None, 150)
small_font = pygame.font.SysFont(None, 40)

# Game variables
score = 0
hits = 0
you_win = False
you_lose = False
death_sound_played = False

# Timer
start_time = pygame.time.get_ticks()
max_time = 5 * 10000 * 6  # 5 seconds in milliseconds

# Asteroid scaling
SIZE_SCALE = {"large": 1.0, "medium": 0.6, "small": 0.3}

# Player setup
player = pygame.Vector2(screen_width/2, screen_height/2)
angle = 180
speed = pygame.Vector2()
player_radius = 20

# Laser, asteroid, and UFO laser lists
lasers = []
laser_speed = 15
asteroids = []
ufos = []  # UFO list
ufos_lasers = []  # lasers fired by UFOs

# Function to create asteroids
def create_asteroid(pos=None, size="large"):
    if pos is None:
        pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
    vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
    return {"pos": pos, "vel": vel, "size": size}

# Function to initialize asteroids
for _ in range(6):
    asteroids.append(create_asteroid())

# Function to create UFO wave of 3
def create_ufos():
    ufos.clear()
    for i in range(3):
        u = {
            'pos': pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height//2)),
            'type': 'tank' if i == 0 else 'shooter',
            'hits': 20 if i == 0 else 3,
            'vel': pygame.Vector2(0.5, 0) if i == 0 else pygame.Vector2(random.choice([-2, 2]), 0),
            'last_shot': 0
        }
        ufos.append(u)

create_ufos()

# Helper to wrap position
def wrap_position(pos):
    if pos.x < 0:
        pos.x = screen_width
    elif pos.x > screen_width:
        pos.x = 0
    if pos.y < 0:
        pos.y = screen_height
    elif pos.y > screen_height:
        pos.y = 0
    return pos

# Restart game state
def restart_game():
    global score, hits, you_win, you_lose, start_time, player, angle, speed
    global lasers, asteroids, ufos, ufos_lasers
    global death_sound_played, waiting_to_start, paused
    global pause_start_time, total_paused_time, second_win

    score = 0
    hits = 0
    you_win = False
    you_lose = False
    death_sound_played = False
    waiting_to_start = False
    paused = False
    pause_start_time = 0
    total_paused_time = 0
    start_time = pygame.time.get_ticks()
    player = pygame.Vector2(screen_width/2, screen_height/2)
    angle = 180
    speed = pygame.Vector2()

    lasers.clear()
    asteroids.clear()
    ufos.clear()
    ufos_lasers.clear()

    for _ in range(6):
        asteroids.append(create_asteroid())
    create_ufos()

# Main game loop
while running:
    screen.blit(background_image, background_rect)

    # Start screen
    if waiting_to_start:
        screen.blit(big_font.render("PLAY", True, (0,255,0)), (screen_width//2-50, screen_height//2-100))
        screen.blit(small_font.render("Enter=Start | P=Pause", True, (255,255,255)), (screen_width//2-120, screen_height//2+50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_to_start = False
                pygame.mixer.music.play(-1)
        continue

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pause_start_time = pygame.time.get_ticks()
                    pygame.mixer.music.pause()
                else:
                    total_paused_time += pygame.time.get_ticks() - pause_start_time
                    pygame.mixer.music.unpause()
            if not paused:
                if event.key == pygame.K_SPACE and not you_win and not you_lose:
                    direction = pygame.Vector2(1, 0).rotate(angle)
                    lasers.append({"pos": player.copy(), "dir": direction})
                    laser_sound.play()
                if event.key == pygame.K_r and you_lose:
                    restart_game()
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_RETURN and you_win:
                    you_win = False
                    second_win = True
                    restart_game()

    # Update timer
    if not you_lose and not paused:
        elapsed = pygame.time.get_ticks() - start_time - total_paused_time
    time_left = max(0, max_time - elapsed)
    if time_left <= 0 and not you_win:
        you_win = True
    seconds_left = time_left // 1000

    # Game updates
    if not waiting_to_start and not paused and not you_win and not you_lose:
        # Player movement
        keys = pygame.key.get_pressed()
        angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
        speed *= 0.75
        player += speed.rotate(angle)
        wrap_position(player)

        # Asteroids
        for asteroid in asteroids[:]:
            asteroid["pos"] += asteroid["vel"]
            wrap_position(asteroid["pos"])
        for laser in lasers[:]:
            laser["pos"] += laser["dir"] * laser_speed
            if not (0 <= laser["pos"].x <= screen_width and 0 <= laser["pos"].y <= screen_height):
                lasers.remove(laser)
        for laser in lasers[:]:
            laser_rect = pygame.Rect(laser["pos"].x, laser["pos"].y, 4, 4)
            for asteroid in asteroids[:]:
                scale = SIZE_SCALE[asteroid["size"]]
                img = pygame.transform.scale(base_astroid_img, (int(60*scale), int(60*scale)))
                rect = img.get_rect(topleft=asteroid["pos"])
                if laser_rect.colliderect(rect):
                    lasers.remove(laser)
                    asteroids.remove(asteroid)
                    score += 10
                    if asteroid["size"] == "large":
                        for _ in range(2):
                            offset = pygame.Vector2(random.randint(-30,30), random.randint(-30,30))
                            asteroids.append(create_asteroid(asteroid["pos"]+offset, "medium"))
                        asteroids.append(create_asteroid(size="large"))
                    elif asteroid["size"] == "medium":
                        for _ in range(2):
                            offset = pygame.Vector2(random.randint(-30,30), random.randint(-30,30))
                            asteroids.append(create_asteroid(asteroid["pos"]+offset, "small"))
                    break
        for asteroid in asteroids[:]:
            scale = SIZE_SCALE[asteroid["size"]]
            img = pygame.transform.scale(base_astroid_img, (int(60*scale), int(60*scale)))
            rect = img.get_rect(topleft=asteroid["pos"])
            if player.distance_to(pygame.Vector2(rect.center)) < player_radius + rect.width/2:
                you_lose = True
                pygame.mixer.music.stop()

        # UFOs behavior
        current = pygame.time.get_ticks()
        for u in ufos[:]:
            u["pos"] += u["vel"]
            wrap_position(u["pos"])
            if u["type"] == "shooter" and current - u["last_shot"] > 4500:
                u["last_shot"] = current
                d = (player - u["pos"]).normalize()
                ufos_lasers.append({"pos": u["pos"].copy(), "dir": d})
                # play UFO laser sound if available
                if ufo_laser_sound:
                    ufo_laser_sound.play()
            screen.blit(ufo_img, u["pos"])
            hp_width = 60 * u["hits"] / (20 if u["type"] == "tank" else 3)
            pygame.draw.rect(screen, (255,0,0), (u["pos"].x, u["pos"].y - 10, hp_width, 5))
            if player.distance_to(u["pos"]) < player_radius + 25:
                you_lose = True
                pygame.mixer.music.stop()
            if u["hits"] <= 0:
                ufos.remove(u)
        # UFO lasers
        for ul in ufos_lasers[:]:
            ul["pos"] += ul["dir"] * 10
            pygame.draw.line(screen, (0,255,0), ul["pos"], ul["pos"] + ul["dir"] * 15, 3)
            # shooter laser hit logic: increment hits and check death threshold
            if player.distance_to(ul["pos"]) < player_radius:
                hits += 1
                ufos_lasers.remove(ul)
                if hits >= 3:
                    you_lose = True
                    pygame.mixer.music.stop()
                continue
            if not (0 <= ul["pos"].x <= screen_width and 0 <= ul["pos"].y <= screen_height):
                ufos_lasers.remove(ul)

    # Draw scene
    if not waiting_to_start:
        # Draw player
        if not you_win and not you_lose:
            pygame.draw.circle(screen, "white", (int(player.x), int(player.y)), player_radius)
            pygame.draw.line(screen, "red", player, player + pygame.Vector2(21,0).rotate(angle))
        # Draw asteroids
        for asteroid in asteroids:
            scale = SIZE_SCALE[asteroid["size"]]
            img = pygame.transform.scale(base_astroid_img, (int(60*scale), int(60*scale)))
            screen.blit(img, asteroid["pos"])
        # Draw lasers
        for laser in lasers:
            pygame.draw.line(screen, "purple", laser["pos"], laser["pos"] + laser["dir"] * 15, 3)
        # HUD
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (screen_width - 200, 20))
        screen.blit(font.render(f"Hits: {hits}/3", True, (255,0,0)), (20,20))
        screen.blit(font.render(f"Time Left: {seconds_left:02}", True, (0,255,0)), (screen_width//2 - 50, screen_height - 60))
        # Win/Lose screens
        if you_win:
            screen.blit(big_font.render("YOU WIN!", True, (255,255,0)), (screen_width//2-200, screen_height//2-100))
            screen.blit(small_font.render("Enter=Continue | ESC=Quit", True, (255,255,255)), (50, screen_height//2))
            planet_img = Second_Winner if second_win else Game_Winner
            screen.blit(pygame.transform.smoothscale(planet_img, (screen_width//2, screen_height)), (screen_width//2,0))
        if you_lose:
            if not death_sound_played:
                death_sound.play()
                death_sound_played = True
            screen.blit(explosion, (player.x-30, player.y-30))
            screen.blit(big_font.render("YOU LOSE", True, (255,0,0)), (screen_width//2-200, screen_height//2-100))
            screen.blit(small_font.render("Press R=Restart or ESC=Quit", True, (255,255,255)), (screen_width//2-150, screen_height//2+50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
