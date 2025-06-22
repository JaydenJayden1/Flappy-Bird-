import pygame
import random

# Initialize pygame
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Load and scale background
background_image = pygame.image.load('Space_S.webp')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_image.get_rect()

# Load and scale asteroid image
astroid_img = pygame.image.load('Astriod-removebg-preview.png')
astroid_img = pygame.transform.scale(astroid_img, (60, 60))
ASTEROID_SIZE = astroid_img.get_rect().size  # (width, height)

# Player setup
player = pygame.Vector2(screen_width, screen_height) / 2
angle = 180
speed = pygame.Vector2()

# Laser setup
lasers = []
laser_speed = 15

# Asteroid setup
asteroid_count = 10
asteroids = []
for _ in range(asteroid_count):
    pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
    vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
    asteroids.append({"pos": pos, "vel": vel})

# Function to wrap around screen edges
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

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                # Shoot a laser in the current direction
                direction = pygame.Vector2(1, 0).rotate(angle)
                lasers.append({
                    "pos": player.copy(),
                    "dir": direction
                })

    # Update player movement
    angle += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    speed.x += keys[pygame.K_UP] - keys[pygame.K_DOWN]
    speed *= 0.75
    player += speed.rotate(angle)
    player = wrap_position(player)

    # Update asteroid positions
    for asteroid in asteroids:
        asteroid["pos"] += asteroid["vel"]
        asteroid["pos"] = wrap_position(asteroid["pos"])

    # Update laser positions
    for laser in lasers[:]:
        laser["pos"] += laser["dir"] * laser_speed
        laser["pos"] = wrap_position(laser["pos"])

    # Check for laser-asteroid collisions
    for laser in lasers[:]:
        laser_rect = pygame.Rect(laser["pos"].x, laser["pos"].y, 4, 4)
        for asteroid in asteroids[:]:
            asteroid_rect = pygame.Rect(asteroid["pos"].x, asteroid["pos"].y, *ASTEROID_SIZE)
            if laser_rect.colliderect(asteroid_rect):
                lasers.remove(laser)
                asteroids.remove(asteroid)

                # Spawn a new asteroid
                new_pos = pygame.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
                new_vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
                asteroids.append({"pos": new_pos, "vel": new_vel})
                break

    # Draw background
    screen.blit(background_image, background_rect)

    # Draw player
    pygame.draw.circle(screen, "white", player, 20)
    pygame.draw.line(screen, "red", player, player + pygame.Vector2(21, 0).rotate(angle))

    # Draw asteroids
    for asteroid in asteroids:
        screen.blit(astroid_img, asteroid["pos"])

    # Draw lasers
    for laser in lasers:
        pygame.draw.line(screen, "purple", laser["pos"], laser["pos"] + laser["dir"] * 15, 3)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
