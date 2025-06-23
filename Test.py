import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Load images
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

base_astroid_img = pygame.image.load('Astriod-removebg-preview.png')
base_astroid_img = pygame.transform.scale(base_astroid_img, (60, 60))

Game_Winner = pygame.image.load('OIP__11_-removebg-preview.png')  # Planet image

# Fonts
font = pygame.font.SysFont(None, 50)
big_font = pygame.font.SysFont(None, 150)
score = 0
hits = 0
you_win = False

# Set timer to 5 minutes
start_time = pygame.time.get_ticks()
max_time = 5 * 60 * 1000  # 5 minutes in milliseconds

# Asteroid scaling
SIZE_SCALE = {
    "large": 1.0,
    "medium": 0.6,
    "small": 0.3
}

# Player setup
player = pygame.Vector2(screen_width, screen_height) / 2
angle = 180
speed = pygame.Vector2()
player_radius = 20

# Laser and asteroid lists
lasers = []
laser_speed = 15
asteroids = []

def create_asteroid(pos=None, size="large"):
    if pos is None:
        pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
    vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
    return {"pos": pos, "vel": vel, "size": size}

# Initial asteroid spawn
for _ in range(6):
    asteroids.append(create_asteroid())

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

# Main game loop
while running:
    elapsed_time = pygame.time.get_ticks() - start_time
    time_left = max(0, max_time - elapsed_time)
    seconds_left = time_left // 1000
    minutes = seconds_left // 60
    seconds = seconds_left % 60

    if time_left == 0 and not you_win:
        you_win = True

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and not you_win:
                direction = pygame.Vector2(1, 0).rotate(angle)
                lasers.append({"pos": player.copy(), "dir": direction})

    if not you_win:
        angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
        speed *= 0.75
        player += speed.rotate(angle)
        player = wrap_position(player)

        for asteroid in asteroids:
            asteroid["pos"] += asteroid["vel"]
            asteroid["pos"] = wrap_position(asteroid["pos"])

        for laser in lasers[:]:
            laser["pos"] += laser["dir"] * laser_speed
            if (laser["pos"].x < 0 or laser["pos"].x > screen_width or
                laser["pos"].y < 0 or laser["pos"].y > screen_height):
                lasers.remove(laser)

        for laser in lasers[:]:
            laser_rect = pygame.Rect(laser["pos"].x, laser["pos"].y, 4, 4)
            for asteroid in asteroids[:]:
                scale = SIZE_SCALE[asteroid["size"]]
                asteroid_img = pygame.transform.scale(base_astroid_img, (
                    int(base_astroid_img.get_width() * scale),
                    int(base_astroid_img.get_height() * scale)
                ))
                asteroid_rect = asteroid_img.get_rect(topleft=asteroid["pos"])
                if laser_rect.colliderect(asteroid_rect):
                    lasers.remove(laser)
                    asteroids.remove(asteroid)
                    score += 10
                    if asteroid["size"] == "large":
                        for _ in range(2):
                            offset = pygame.Vector2(random.randint(-30, 30), random.randint(-30, 30))
                            asteroids.append(create_asteroid(asteroid["pos"] + offset, "medium"))
                        asteroids.append(create_asteroid(size="large"))
                    elif asteroid["size"] == "medium":
                        for _ in range(2):
                            offset = pygame.Vector2(random.randint(-30, 30), random.randint(-30, 30))
                            asteroids.append(create_asteroid(asteroid["pos"] + offset, "small"))
                    break

        for asteroid in asteroids[:]:
            scale = SIZE_SCALE[asteroid["size"]]
            asteroid_img = pygame.transform.scale(base_astroid_img, (
                int(base_astroid_img.get_width() * scale),
                int(base_astroid_img.get_height() * scale)
            ))
            asteroid_rect = asteroid_img.get_rect(topleft=asteroid["pos"])
            distance = player.distance_to(pygame.Vector2(asteroid_rect.center))
            if distance < player_radius + max(asteroid_rect.width, asteroid_rect.height) / 2:
                hits += 1
                print(f"Hit {hits}/3")
                asteroids.remove(asteroid)
                pygame.time.delay(300)
                if hits >= 3:
                    print("Game Over: You hit 3 asteroids!")
                    pygame.quit()
                    sys.exit()
                break

    # Draw everything
    screen.blit(background_image, background_rect)

    if not you_win:
        pygame.draw.circle(screen, "white", player, player_radius)
        pygame.draw.line(screen, "red", player, player + pygame.Vector2(21, 0).rotate(angle))

    for asteroid in asteroids:
        scale = SIZE_SCALE[asteroid["size"]]
        scaled_img = pygame.transform.scale(base_astroid_img, (
            int(base_astroid_img.get_width() * scale),
            int(base_astroid_img.get_height() * scale)
        ))
        screen.blit(scaled_img, asteroid["pos"])

    for laser in lasers:
        pygame.draw.line(screen, "purple", laser["pos"], laser["pos"] + laser["dir"] * 15, 3)

    # HUD
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
    hits_surface = font.render(f"Hits: {hits}/3", True, (255, 0, 0))
    timer_surface = font.render(f"Time Left: {minutes:02}:{seconds:02}", True, (0, 255, 0))
    screen.blit(score_surface, (screen_width - score_surface.get_width() - 20, 20))
    screen.blit(hits_surface, (20, 20))
    screen.blit(timer_surface, (screen_width // 2 - timer_surface.get_width() // 2, screen_height - 60))

    # YOU WIN and big planet on right half of screen
    if you_win:
        win_text = big_font.render("YOU WIN!", True, (255, 255, 0))
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 100))

        planet_width = screen_width // 2
        planet_height = screen_height
        planet_scaled = pygame.transform.smoothscale(Game_Winner, (planet_width, planet_height))
        planet_x = screen_width - planet_width
        planet_y = 0
        screen.blit(planet_scaled, (planet_x, planet_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
